from __future__ import annotations

import csv
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

import eval_runner  # noqa: E402


class EvalRunnerTests(unittest.TestCase):
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
            rc = eval_runner.main(list(args))
        return rc, buf.getvalue()

    def test_work_id_determinism(self) -> None:
        expected = "6b4370a895a4fc75"
        self.assertEqual(eval_runner.compute_work_id("med-001", "claude-opus-4.7-high", 0), expected)
        self.assertEqual(
            eval_runner.compute_work_id("med-001", "claude-opus-4.7-high", 0),
            eval_runner.compute_work_id("med-001", "claude-opus-4.7-high", 0),
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
        prompts = eval_runner.load_jsonl(self.prompts)
        models = eval_runner.load_models(self.models)
        work_id = eval_runner.compute_work_id("p1", "m1", 0)
        self.out_dir.mkdir(parents=True)
        (self.out_dir / f"{work_id}.json").write_text('{"already": true}\n', encoding="utf-8")
        plan, skipped = eval_runner.build_plan(prompts, models, 1, self.out_dir, resume=True)
        self.assertEqual(skipped, 1)
        self.assertEqual(len(plan), 3)
        self.assertNotIn(work_id, {item["work_id"] for item in plan})

    def test_mock_writes_complete_valid_record(self) -> None:
        rc, out = self.run_main(
            "--mock",
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
        self.assertTrue(record["response_text"].startswith("[MOCK] "))
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
        self.assertIn("Prompts     :", out)
        self.assertIn("(1 prompts)", out)
        self.assertIn("(2 models)", out)
        self.assertIn("Planned     : 4 runs", out)


if __name__ == "__main__":
    unittest.main()
