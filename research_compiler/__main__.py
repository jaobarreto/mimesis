import argparse
import json
import sqlite3
import sys
from pathlib import Path

from .projection import compile_package


def main():
    parser = argparse.ArgumentParser(description="Compilar o pacote local de Research em SQLite.")
    parser.add_argument("package", type=Path, help="diretório que contém manifest.json")
    parser.add_argument("output", type=Path, help="arquivo .sqlite de destino")
    parser.add_argument("--manifest-sha256", required=True, help="digest esperado da edição")
    args = parser.parse_args()
    try:
        receipt = compile_package(args.package, args.output, args.manifest_sha256)
    except (OSError, ValueError, sqlite3.Error, RecursionError) as exc:
        print(f"Pacote recusado: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
