"""CLI local de recuperação sobre fixtures de desenvolvimento."""

import argparse
import json
import sqlite3
import sys

from .engine import Experiment
from .retrieval import RETRIEVERS


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture",
        action="store_true",
        required=True,
        help="habilita explicitamente a projeção sintética isolada",
    )
    parser.add_argument("--method", choices=RETRIEVERS, required=True)
    parser.add_argument("text", help="texto de uma consulta pt-BR")
    args = parser.parse_args(argv)
    try:
        with Experiment() as engine:
            result = engine.query(args.text, args.method)
    except sqlite3.Error as exc:
        print(
            json.dumps(
                {
                    "mode": "experimental_fixture",
                    "outcome": "unavailable",
                    "algorithm": args.method,
                    "reason": "sqlite_error",
                    "detail": str(exc),
                },
                ensure_ascii=True,
            )
        )
        return 1
    print(json.dumps(result, ensure_ascii=True, indent=2, allow_nan=False))
    return 2 if result["outcome"] == "invalid_input" else 0


if __name__ == "__main__":
    sys.exit(main())
