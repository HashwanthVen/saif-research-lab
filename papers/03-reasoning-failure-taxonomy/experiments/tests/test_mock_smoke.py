"""Tests for the SMOKE-ONLY mock runner.

These tests guarantee the smoke harness:
  - keeps the work_id formula bit-for-bit identical with the PS1 runner,
  - never invokes a real CLI (no subprocess imports allowed),
  - writes records that are self-tagged as mock,
  - supports --resume and filtering semantics.
"""
from __future__ import annotations

import io
import json
import shutil
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import mock_smoke  # noqa: E402


class MockSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.work = ROOT / ".test_work" / self._testMethodName
        if self.work.exists():
            shutil.rmtree(self.work)
        self.work.mkdir(parents=True)
        self.prompts = self.work / "prompts.jsonl"
        self.models = self.work / "models.json"
        self.out_dir = self.work / "runs"
        prompt_rows = [
            {"prompt_id": "p1", "domain": "medicine", "difficulty": "mid", "prompt_text": "Prompt one", "ground_truth_keywords": ["alpha"]},
            {"prompt_id": "p2", "domain": "legal", "difficulty": "high", "prompt_text": "Prompt two", "ground_truth_keywords": ["beta"]},
        ]
        self.prompts.write_text("\n".join(json.dumps(r) for r in prompt_rows) + "\n", encoding="utf-8")
        self.models.write_text(
            json.dumps(
                {
                    "models": [
                        {"cli_id": "m1", "display": "Model 1", "tier": "frontier", "thinking": True, "include": True},
                        {"cli_id": "m2", "display": "Model 2", "tier": "mid", "thinking": False, "include": True},
                        {"cli_id": "m3", "display": "Model 3", "tier": "small", "thinking": False, "include": False},
                    ]
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.work.parent, ignore_errors=True)

    def run_main(self, *args: str) -> tuple[int, str]:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = mock_smoke.main(list(args))
        return rc, buf.getvalue()

    def test_no_subprocess_import(self) -> None:
        """The smoke runner must never import subprocess; that would make it
        possible to invoke a real CLI from this module, which violates the
        hard constraint that all real evaluation goes through eval_runner.ps1."""
        src = (SRC / "mock_smoke.py").read_text(encoding="utf-8")
        self.assertNotIn("import subprocess", src)
        self.assertNotIn("from subprocess", src)

    def test_no_network_imports(self) -> None:
        """The smoke runner must not import any networking module. The module
        docstring promises 'no network access'; this regression test enforces
        it so the smoke harness cannot quietly grow a path that exfiltrates
        prompts to an HTTP endpoint."""
        src = (SRC / "mock_smoke.py").read_text(encoding="utf-8")
        forbidden = [
            "import requests", "from requests",
            "import urllib", "from urllib",
            "import http", "from http",
            "import httpx", "from httpx",
            "import socket as ", "from socket import",  # socket.gethostname() is the only allowed use; star-imports / aliased imports are not
            "import aiohttp", "from aiohttp",
        ]
        for needle in forbidden:
            self.assertNotIn(needle, src, f"Forbidden network import detected: {needle!r}")

    def test_work_id_determinism_matches_ps1_formula(self) -> None:
        """work_id formula must stay bit-for-bit identical with eval_runner.ps1."""
        expected = "6b4370a895a4fc75"
        self.assertEqual(mock_smoke.compute_work_id("med-001", "claude-opus-4.7-high", 0), expected)
        self.assertEqual(
            mock_smoke.compute_work_id("med-001", "claude-opus-4.7-high", 0),
            mock_smoke.compute_work_id("med-001", "claude-opus-4.7-high", 0),
        )

    def test_dry_run_plan_count(self) -> None:
        rc, out = self.run_main(
            "--dry-run",
            "--prompts", str(self.prompts),
            "--models", str(self.models),
            "--out-dir", str(self.out_dir),
            "--num-seeds", "3",
        )
        self.assertEqual(rc, 0)
        self.assertIn("Planned     : 12 runs", out)
        self.assertFalse(self.out_dir.exists())

    def test_resume_skips_existing_files(self) -> None:
        prompts = mock_smoke.load_jsonl(self.prompts)
        models = mock_smoke.load_models(self.models)
        work_id = mock_smoke.compute_work_id("p1", "m1", 0)
        self.out_dir.mkdir(parents=True)
        (self.out_dir / f"{work_id}.json").write_text('{"already": true}\n', encoding="utf-8")
        plan, skipped = mock_smoke.build_plan(prompts, models, 1, self.out_dir, resume=True)
        self.assertEqual(skipped, 1)
        self.assertEqual(len(plan), 3)
        self.assertNotIn(work_id, {item["work_id"] for item in plan})

    def test_record_is_self_tagged_as_mock(self) -> None:
        rc, out = self.run_main(
            "--prompts", str(self.prompts),
            "--models", str(self.models),
            "--out-dir", str(self.out_dir),
            "--num-seeds", "1",
            "--models-filter", "m1",
            "--prompts-filter", "p1",
        )
        self.assertEqual(rc, 0, out)
        files = sorted(self.out_dir.glob("*.json"))
        self.assertEqual(len(files), 1)
        record = json.loads(files[0].read_text(encoding="utf-8"))
        required = {
            "work_id", "prompt_id", "domain", "difficulty", "cli_id", "display", "tier", "thinking",
            "seed", "prompt_text", "response_text", "stderr", "exit_code", "timed_out", "duration_sec",
            "started_at", "finished_at", "cli_invocation", "machine", "user", "python_version", "script_version",
        }
        self.assertTrue(required.issubset(record.keys()))
        self.assertEqual(record["exit_code"], 0)
        self.assertFalse(record["timed_out"])
        # Self-tagging contract: any downstream consumer can filter on these markers
        # to refuse to treat the record as real evidence.
        self.assertTrue(record["response_text"].startswith("[MOCK] "))
        self.assertIn("mock_smoke.py", record["script_version"])
        self.assertIn("MOCK", record["cli_invocation"])
        progress = (self.out_dir / "_progress.tsv").read_text(encoding="utf-8").strip().split("\t")
        self.assertEqual(progress[5], "ok")

    def test_filters_narrow_plan(self) -> None:
        rc, out = self.run_main(
            "--dry-run",
            "--prompts", str(self.prompts),
            "--models", str(self.models),
            "--out-dir", str(self.out_dir),
            "--num-seeds", "2",
            "--models-filter", "m1,m3",
            "--prompts-filter", "p2",
        )
        self.assertEqual(rc, 0)
        self.assertIn("(1 prompts)", out)
        self.assertIn("(2 models)", out)
        self.assertIn("Planned     : 4 runs", out)


if __name__ == "__main__":
    unittest.main()
