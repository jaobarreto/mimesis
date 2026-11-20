"""Registro local do piloto. O SQLite editorial é independente da projeção do motor."""

import csv
import hashlib
import io
import json
import sqlite3
import unicodedata
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from .importer import strict_json_loads as read_json

Text = Annotated[str, StringConstraints(min_length=1)]
INTENTS = Literal[
    "Greeting",
    "Farewell",
    "Gratitude",
    "Introduction",
    "Help Request",
    "Permission Request",
    "Information Request",
    "Apology",
    "Agreement",
    "Disagreement",
]


class Candidate(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    id: Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_-]+$")]
    revision: int = Field(default=1, ge=1)
    intent: INTENTS
    prompts: list[Text] = Field(min_length=1)
    responses: list[Text] = Field(min_length=1)

    @field_validator("prompts", "responses")
    @classmethod
    def unique_text(cls, values):
        keys = {normalize(v) for v in values}
        if "" in keys or len(keys) != len(values):
            raise ValueError("texto vazio ou duplicado na família")
        return values


def normalize(text):
    folded = unicodedata.normalize("NFC", text).casefold()
    return " ".join(unicodedata.normalize("NFC", folded).split())


def now():
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode(obj):
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
    pragma foreign_keys=on;
    create table if not exists artifact(
      hash text primary key, source text not null, creator text not null, original blob not null,
      acquired text not null);
    create table if not exists candidate(
      id text, rev integer, hash text references artifact(hash), line integer,
      intent text, data text, primary key(id,rev));
    create table if not exists ballot(
      id text, rev integer, reviewer text, prompt integer, response integer,
      verdict text, reason text, at text, primary key(id,rev,reviewer,prompt,response),
      foreign key(id,rev) references candidate(id,rev));
    create table if not exists curation(id text,rev integer,actor text,group_id text,
      evidence_sha256 text,decision blob,at text,primary key(id,rev),
      foreign key(id,rev) references candidate(id,rev));
    create table if not exists edition(version text primary key, manifest_sha256 text not null,
      decision_sha256 text not null, manifest blob not null);
    """)
    return db


def prepare(db, pilot):
    # The two identified synthetic sources are authorized for this local research task.
    sources = [
        ("contribution", "ChatGPT, contribuição sintética fornecida pelo solicitante"),
        ("codex", "Codex, geração sintética para dlg-pilot-001"),
    ]
    with db:
        for source, creator in sources:
            data = (pilot / f"{source}.jsonl").read_bytes()
            sha = digest(data)
            db.execute(
                "insert or ignore into artifact values(?,?,?,?,?)",
                (sha, source, creator, data, now()),
            )
            seen = set()
            for line, raw in enumerate(data.decode("utf-8").splitlines(), 1):
                record = Candidate.model_validate(read_json(raw))
                key = (record.id, record.revision)
                if key in seen:
                    raise ValueError(f"identidade repetida {key}")
                seen.add(key)
                prior = db.execute(
                    "select * from candidate where id=? and rev=?", key
                ).fetchone()
                if prior:
                    prior_source = db.execute(
                        "select source from artifact where hash=?", (prior["hash"],)
                    ).fetchone()[0]
                    if (
                        prior_source != source
                        or Candidate.model_validate_json(prior["data"]) != record
                    ):
                        raise ValueError(f"revisão imutável {key}")
                    continue
                previous = db.execute(
                    "select max(rev) from candidate where id=?", (record.id,)
                ).fetchone()[0]
                if record.revision != (previous or 0) + 1:
                    raise ValueError(f"sequência de revisões inválida {key}")
                db.execute(
                    "insert into candidate values(?,?,?,?,?,?)",
                    (*key, sha, line, record.intent, record.model_dump_json()),
                )


def current(db):
    return db.execute("""select c.* from candidate c where rev=(
      select max(rev) from candidate p where p.id=c.id) order by id""").fetchall()


FIELDS = [
    "id",
    "revision",
    "artifact_sha256",
    "prompt_id",
    "response_id",
    "prompt",
    "response",
    "intent",
    "verdict",
    "reason",
]


def matrix(row):
    record = Candidate.model_validate_json(row["data"])
    for i, prompt in enumerate(record.prompts, 1):
        for j, response in enumerate(record.responses, 1):
            yield [
                record.id,
                str(record.revision),
                row["hash"],
                f"{record.id}-p{i}",
                f"{record.id}-r{j}",
                prompt,
                response,
                record.intent,
                "",
                "",
            ]


def sheet(db, output):
    with output.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(FIELDS)
        for row in current(db):
            writer.writerows(matrix(row))


def vote(db, reviewer, file):
    if not reviewer.strip():
        raise ValueError("identifique o revisor")
    source = csv.reader(io.StringIO(file.read_text(encoding="utf-8-sig"), newline=""))
    if next(source, []) != FIELDS:
        raise ValueError("cabeçalho de revisão inválido")
    reviewer = normalize(reviewer)
    with db:
        db.execute("begin immediate")
        expected = {
            tuple(pair[:5]): pair for row in current(db) for pair in matrix(row)
        }
        for pair in source:
            if (
                len(pair) != len(FIELDS)
                or expected.get(tuple(pair[:5]), [])[:8] != pair[:8]
            ):
                raise ValueError("par ausente, alterado ou obsoleto")
            verdict, reason = pair[-2:]
            if not verdict and not reason:
                continue
            if verdict not in {"accept", "reject"} or not reason.strip():
                raise ValueError("preencha accept/reject e a justificativa")
            participants = {
                r[0]
                for r in db.execute(
                    "select distinct reviewer from ballot where id=? and rev=?",
                    pair[:2],
                )
            }
            if len(participants) >= 2 and reviewer.strip() not in participants:
                raise ValueError(
                    "dois revisores já atribuídos; divergência requer adjudicação"
                )
            key = (
                pair[0],
                int(pair[1]),
                reviewer.strip(),
                int(pair[3].rsplit("-p", 1)[1]),
                int(pair[4].rsplit("-r", 1)[1]),
            )
            old = db.execute(
                """select verdict,reason from ballot where
              (id,rev,reviewer,prompt,response)=(?,?,?,?,?)""",
                key,
            ).fetchone()
            if old and tuple(old) != (verdict, reason):
                raise ValueError("parecer já registrado com outro conteúdo")
            db.execute(
                "insert or ignore into ballot values(?,?,?,?,?,?,?,?)",
                (*key, verdict, reason, now()),
            )


def review(db, row):
    """Somente dois pareceres integrais concordantes encerram a revisão de pares."""
    ballots = db.execute(
        "select * from ballot where id=? and rev=? order by reviewer",
        (row["id"], row["rev"]),
    ).fetchall()
    reviewers = sorted({b["reviewer"] for b in ballots})
    n = sum(1 for _ in matrix(row))
    if len(reviewers) != 2 or len(ballots) != n * len(reviewers):
        return "pending", reviewers
    votes = {}
    for b in ballots:
        votes.setdefault((b["prompt"], b["response"]), set()).add(b["verdict"])
    if any(len(v) != 1 for v in votes.values()):
        from .adjudication import resolved

        return resolved(db, row) or ("disputed", reviewers)
    return (
        "rejected" if any("reject" in v for v in votes.values()) else "accepted"
    ), reviewers
