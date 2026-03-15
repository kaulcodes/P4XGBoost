from __future__ import annotations

from pathlib import Path
import sys


if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from evaluation.ablation import build_ablation_summary_text
    from evaluation.figures import generate_all_figures
    from evaluation.logs import write_replication_log
    from evaluation.paths import ensure_directories
    from evaluation.summary import write_summary_json
    from evaluation.tables import render_all_tables
else:
    from .ablation import build_ablation_summary_text
    from .figures import generate_all_figures
    from .logs import write_replication_log
    from .paths import ensure_directories
    from .summary import write_summary_json
    from .tables import render_all_tables


def main() -> None:
    ensure_directories()
    render_all_tables()
    print("\n--- Ablation Summary ---")
    print(build_ablation_summary_text())
    generated_files = generate_all_figures()
    write_summary_json([str(path) for path in generated_files])
    write_replication_log(generated_files)
    print("\n[SUCCESS] Replication artifacts generated successfully.")


if __name__ == "__main__":
    main()
