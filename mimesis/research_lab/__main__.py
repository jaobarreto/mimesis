"""Inicialização do Streamlit restrita à interface de loopback."""

import os
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    os.environ["PYTHONPATH"] = str(root)
    os.execv(
        sys.executable,
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(root / "research_lab/app.py"),
            "--server.address=127.0.0.1",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
            "--server.fileWatcherType=none",
        ],
    )


if __name__ == "__main__":
    main()
