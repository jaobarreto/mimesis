"""Empacota a CLI experimental em um arquivo .pyz executável com Python."""

import argparse
import io
import shutil
import tempfile
import zipapp
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build(output):
    with tempfile.TemporaryDirectory() as directory:
        stage = Path(directory)
        for name in ("research_experiment", "research_compiler"):
            shutil.copytree(
                ROOT / name, stage / name, ignore=shutil.ignore_patterns("__pycache__")
            )
        (stage / "__main__.py").write_text(
            "from research_experiment.__main__ import main\nraise SystemExit(main())\n",
            encoding="utf-8",
        )
        archive = io.BytesIO()
        zipapp.create_archive(stage, archive, compressed=True)
        with output.open("xb") as target:
            target.write(archive.getbuffer())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.output)
