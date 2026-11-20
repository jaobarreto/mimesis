"""Porta de entrada das ferramentas editoriais de Research."""

import argparse
import json
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

from . import pilot, release


def stats(db):
    import duckdb
    import polars as pl

    rows = []
    for row in pilot.current(db):
        rec = pilot.Candidate.model_validate_json(row["data"])
        state, _ = pilot.review(db, row)
        rows.append(
            (
                rec.intent,
                len(rec.prompts),
                len(rec.responses),
                len(rec.prompts) * len(rec.responses),
                state,
            )
        )
    frame = pl.DataFrame(
        rows,
        schema={
            "intent": pl.String,
            "prompts": pl.Int64,
            "responses": pl.Int64,
            "pairs": pl.Int64,
            "state": pl.String,
        },
        orient="row",
    )
    categories = (
        frame.group_by("intent")
        .agg(
            pl.len().alias("talksets"),
            pl.col("prompts").sum(),
            pl.col("responses").sum(),
            pl.col("pairs").sum(),
        )
        .sort("intent")
        .to_dicts()
    )
    with duckdb.connect() as counts:
        counts.execute("create table reviews(state varchar)")
        if rows:
            counts.executemany(
                "insert into reviews values (?)", [(r[-1],) for r in rows]
            )
        review_counts = dict(
            counts.execute(
                "select state,count(*) from reviews group by state"
            ).fetchall()
        )
    releases = set()
    for (manifest,) in db.execute("select manifest from edition"):
        releases.update(
            (r["record_id"], r["revision"])
            for r in pilot.read_json(manifest)["records"]
        )
    return {
        "talksets": len(rows),
        "synthetic": len(rows),
        "prompts": sum(r[1] for r in rows),
        "responses": sum(r[2] for r in rows),
        "pairs": sum(r[3] for r in rows),
        "pair_reviews": review_counts,
        "curated_revisions_ever": db.execute(
            "select count(*) from curation"
        ).fetchone()[0],
        "released_revisions_ever": len(releases),
        "categories": categories,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("work/editorial.sqlite"))
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("prepare", "audit"):
        p = sub.add_parser(name)
        p.add_argument("--pilot", type=Path, default=Path("pilot"))
    sub.add_parser("stats")
    for name in ("sheet", "candidates", "catalog"):
        sub.add_parser(name).add_argument("output", type=Path)
    p = sub.add_parser("vote")
    p.add_argument("reviewer")
    p.add_argument("file", type=Path)
    p = sub.add_parser("adjudicate")
    p.add_argument("record_id")
    p.add_argument("revision", type=int)
    p.add_argument("actor")
    p.add_argument("verdict", choices=["accept", "reject"])
    p.add_argument("reason", type=Path)
    sub.add_parser("curate").add_argument("decision", type=Path)
    p = sub.add_parser("export")
    p.add_argument("decision", type=Path)
    p.add_argument("destination", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.cmd == "audit":
            from .audit import audit

            result = audit(args.pilot)
        else:
            with closing(pilot.connect(args.db)) as db:
                if args.cmd == "prepare":
                    pilot.prepare(db, args.pilot)
                    result = stats(db)
                elif args.cmd == "stats":
                    result = stats(db)
                elif args.cmd == "catalog":
                    from .catalog import write

                    write(db, args.output)
                    result = {"output": str(args.output)}
                elif args.cmd == "candidates":
                    release.candidates(db, args.output)
                    result = {"output": str(args.output)}
                elif args.cmd == "sheet":
                    pilot.sheet(db, args.output)
                    result = {"output": str(args.output)}
                elif args.cmd == "vote":
                    pilot.vote(db, args.reviewer, args.file)
                    result = stats(db)
                elif args.cmd == "adjudicate":
                    from .adjudication import adjudicate

                    verdict, reviewers = adjudicate(
                        db,
                        args.record_id,
                        args.revision,
                        args.actor,
                        args.verdict,
                        pilot.read_json(args.reason.read_text()),
                    )
                    result = {"decision": verdict, "reviewers": reviewers}
                elif args.cmd == "curate":
                    release.curate(db, args.decision)
                    result = stats(db)
                elif args.cmd == "export":
                    result = {
                        "manifest_sha256": release.export(
                            db, args.decision, args.destination
                        )
                    }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return int(args.cmd == "audit" and result["blocked"])
    except (ValueError, KeyError, TypeError, OSError, sqlite3.Error) as exc:
        print(f"Operação recusada: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
