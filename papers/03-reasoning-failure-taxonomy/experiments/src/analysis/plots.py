"""Generate Paper 03 analysis plots from table outputs.

Requires matplotlib. If tables are empty or matplotlib is unavailable, this
script prints a TODO message and exits successfully.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

PAPER_DIR = Path(__file__).resolve().parents[3]
DEFAULT_TABLES = PAPER_DIR / "results" / "tables"
DEFAULT_FIGURES = PAPER_DIR / "figures"
F_CODES = ["F1", "F2", "F3", "F4"]
COLORS = {"": "#eeeeee", "F1": "#d73027", "F2": "#fc8d59", "F3": "#91bfdb", "F4": "#4575b4"}


def read_csv(path: Path) -> list[dict[str, Any]]:
    """Read CSV rows or return empty list if missing."""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def save_both(fig: Any, figures_dir: Path, stem: str) -> None:
    """Save a matplotlib figure to PDF and PNG."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(figures_dir / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(figures_dir / f"{stem}.png", dpi=200, bbox_inches="tight")


def plot_heatmap(rows: list[dict[str, Any]], figures_dir: Path, plt: Any) -> bool:
    """Plot domain x model heatmap colored by dominant F-code."""
    if not rows:
        print("TODO: failure_mode_distribution.csv is empty; skipping heatmap.")
        return False
    grouped: dict[tuple[str, str], dict[str, float]] = {}
    for row in rows:
        cli = str(row.get("cli_id", ""))
        domain = str(row.get("domain", ""))
        code = str(row.get("f_code", ""))
        try:
            frac = float(row.get("fraction", "") or 0.0)
        except ValueError:
            frac = 0.0
        grouped.setdefault((domain, cli), {})[code] = frac
    domains = sorted({d for d, _ in grouped})
    models = sorted({m for _, m in grouped})
    if not domains or not models:
        print("TODO: no domain/model cells for heatmap.")
        return False

    fig_w = max(8, len(models) * 1.2)
    fig_h = max(5, len(domains) * 0.8)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    for y, domain in enumerate(domains):
        for x, model in enumerate(models):
            scores = grouped.get((domain, model), {})
            best_score = max((scores.get(c, 0.0) for c in F_CODES), default=0.0)
            dominant = max(F_CODES, key=lambda c: scores.get(c, 0.0)) if best_score > 0 else ""
            rect = plt.Rectangle((x, y), 1, 1, facecolor=COLORS.get(dominant, "#eeeeee"), edgecolor="white")
            ax.add_patch(rect)
            label = dominant if dominant else "NA"
            ax.text(x + 0.5, y + 0.5, label, ha="center", va="center", fontsize=9)
    ax.set_xlim(0, len(models))
    ax.set_ylim(0, len(domains))
    ax.set_xticks([i + 0.5 for i in range(len(models))], models, rotation=45, ha="right")
    ax.set_yticks([i + 0.5 for i in range(len(domains))], domains)
    ax.invert_yaxis()
    ax.set_title("Dominant failure mode by domain and model")
    ax.set_xlabel("Model")
    ax.set_ylabel("Domain")
    save_both(fig, figures_dir, "failure_mode_heatmap")
    plt.close(fig)
    print(f"Wrote failure_mode_heatmap.pdf/png to {figures_dir}")
    return True


def plot_calibration(rows: list[dict[str, Any]], figures_dir: Path, plt: Any) -> bool:
    """Plot reliability curves from confidence_calibration_bins.csv."""
    if not rows:
        print("TODO: confidence_calibration_bins.csv is empty/missing; skipping calibration curves.")
        return False
    domains = sorted({str(r.get("domain", "")) for r in rows})
    if not domains:
        print("TODO: no domains in calibration bins; skipping calibration curves.")
        return False
    ncols = min(3, len(domains))
    nrows = (len(domains) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows), squeeze=False)
    for ax in axes.flat:
        ax.axis("off")
    for idx, domain in enumerate(domains):
        ax = axes[idx // ncols][idx % ncols]
        ax.axis("on")
        ax.plot([0, 1], [0, 1], linestyle="--", color="gray", linewidth=1)
        domain_rows = [r for r in rows if str(r.get("domain", "")) == domain]
        models = sorted({str(r.get("cli_id", "")) for r in domain_rows})
        for model in models:
            pts = []
            for row in domain_rows:
                if str(row.get("cli_id", "")) != model:
                    continue
                try:
                    n = int(row.get("n", "0") or 0)
                    acc = float(row.get("accuracy", "nan"))
                    conf = float(row.get("mean_confidence", "nan"))
                except ValueError:
                    continue
                if n > 0 and acc == acc and conf == conf:
                    pts.append((conf, acc))
            pts.sort()
            if pts:
                ax.plot([p[0] for p in pts], [p[1] for p in pts], marker="o", label=model)
        ax.set_title(domain)
        ax.set_xlabel("Mean confidence")
        ax.set_ylabel("Empirical accuracy")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        if models:
            ax.legend(fontsize=7)
    fig.suptitle("Confidence calibration reliability curves")
    save_both(fig, figures_dir, "calibration_curves")
    plt.close(fig)
    print(f"Wrote calibration_curves.pdf/png to {figures_dir}")
    return True


def main() -> int:
    """CLI entry point."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tables-dir", type=Path, default=DEFAULT_TABLES)
    ap.add_argument("--figures-dir", type=Path, default=DEFAULT_FIGURES)
    args = ap.parse_args()

    try:
        import matplotlib.pyplot as plt  # type: ignore
    except ImportError as exc:
        print(f"TODO: matplotlib unavailable ({exc}); skipping plots.")
        return 0

    fm_rows = read_csv(args.tables_dir / "failure_mode_distribution.csv")
    bin_rows = read_csv(args.tables_dir / "confidence_calibration_bins.csv")
    plot_heatmap(fm_rows, args.figures_dir, plt)
    plot_calibration(bin_rows, args.figures_dir, plt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
