import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent


def run_ui() -> int:
    return subprocess.call(
        [sys.executable, "-m", "streamlit", "run", str(ROOT_DIR / "ui_app.py")],
        cwd=str(ROOT_DIR),
    )


def run_cli() -> int:
    from autosync import main

    main()
    return 0


def run_bulk() -> int:
    from bulk_generate import main

    main()
    return 0


def run_status() -> int:
    from services.system_service import get_status

    print(json.dumps(get_status(), ensure_ascii=True, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run current LeetCode AutoSync workflows")
    parser.add_argument(
        "mode",
        choices=["ui", "cli", "bulk", "status"],
        help="Workflow mode to run",
    )
    args = parser.parse_args()

    if args.mode == "ui":
        return run_ui()
    if args.mode == "cli":
        return run_cli()
    if args.mode == "bulk":
        return run_bulk()
    return run_status()


if __name__ == "__main__":
    raise SystemExit(main())
