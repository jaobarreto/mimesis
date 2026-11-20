"""Exportação do envelope e seleção explícita de uma edição local de Research."""

import os
import re
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

from .pilot import Candidate, current, digest, encode, read_json, review

PROFILE = "research-dlg-v1"
SCHEMA = "0.1.0"
SCOPES = {
    "access",
    "internal_copy",
    "extraction",
    "transformation",
    "local_query",
    "redistribution",
}


def describe(row, artifact):
    rec = Candidate.model_validate_json(row["data"])
    provenance = {
        "artifact_id": artifact["hash"],
        "locator": f"line:{row['line']}",
        "activity_ids": [f"process-{rec.id}-{rec.revision}"],
    }
    return {
        "record_id": rec.id,
        "revision": rec.revision,
        "domain": "MKB-DLG",
        "schema_version": SCHEMA,
        "language": "pt-BR",
        "source_id": artifact["source"],
        "rights_id": f"rights-{artifact['hash']}",
        "provenance": provenance,
        "status": "PROCESSED",
        "payload": {
            "prompts": [
                {"prompt_id": f"{rec.id}-p{i}", "text": t}
                for i, t in enumerate(rec.prompts, 1)
            ],
            "responses": [
                {"response_id": f"{rec.id}-r{i}", "text": t}
                for i, t in enumerate(rec.responses, 1)
            ],
        },
    }


def source_for(db, row):
    a = db.execute("select * from artifact where hash=?", (row["hash"],)).fetchone()
    if not a or digest(a["original"]) != row["hash"]:
        raise ValueError("original ausente ou alterado")
    origin = Candidate.model_validate(
        read_json(a["original"].decode().splitlines()[row["line"] - 1])
    )
    if origin != Candidate.model_validate_json(row["data"]):
        raise ValueError("registro diverge do localizador")
    return a


def candidates(db, output):
    rows = []
    for row in current(db):
        record = describe(row, source_for(db, row))
        if review(db, row)[0] == "rejected":
            record["status"] = "REJECTED"
        elif db.execute(
            "select 1 from curation where id=? and rev=?", (row["id"], row["rev"])
        ).fetchone():
            record["status"] = "CURATED"
        rows.append(encode(record) + b"\n")
    with output.open("xb") as f:
        f.writelines(rows)


def evidence(base, obj):
    path = (base / obj["evidence_locator"]).resolve()
    if not path.is_relative_to(base.resolve()) or not path.is_file():
        raise ValueError("evidência local ausente")
    if digest(path.read_bytes()) != obj["evidence_sha256"]:
        raise ValueError("digest da evidência divergente")


def utc(value):
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("instante UTC com Z obrigatório")
    datetime.fromisoformat(value)
    return value


def nonempty(obj, fields):
    for key in fields:
        if not isinstance(obj.get(key), str) or not obj[key].strip():
            raise ValueError(f"campo obrigatório {key}")


def curate(db, decision_file):
    """Registrar a decisão editorial e o grupo de origem após os pareceres."""
    decision = read_json(decision_file.read_text())
    nonempty(decision, ["actor", "group_id", "record_id", "artifact_sha256"])
    if decision["decision"] != "curate" or decision["internal_research"] != "allowed":
        raise ValueError("curadoria requer permissão para pesquisa interna")
    utc(decision["reviewed_at"])
    evidence(decision_file.parent, decision)
    key = (decision["record_id"], decision["revision"])
    with db:
        db.execute("begin immediate")
        row = db.execute("select * from candidate where id=? and rev=?", key).fetchone()
        if (
            not row
            or row["hash"] != decision["artifact_sha256"]
            or review(db, row)[0] != "accepted"
        ):
            raise ValueError("curadoria exige a revisão correta e pares aceitos")
        source_for(db, row)
        prior = db.execute(
            "select decision from curation where id=? and rev=?", key
        ).fetchone()
        if prior and prior[0] != encode(decision):
            raise ValueError("decisão de curadoria imutável")
        db.execute(
            "insert or ignore into curation values(?,?,?,?,?,?,?)",
            (
                *key,
                decision["actor"],
                decision["group_id"],
                decision["evidence_sha256"],
                encode(decision),
                decision["reviewed_at"],
            ),
        )


def export(db, decision_file, destination):
    with db:
        db.execute("begin immediate")
        return _export(db, decision_file, destination)


def _export(db, decision_file, destination):
    """A declaração do mantenedor é entrada confiada, sob custódia local."""
    decision = read_json(decision_file.read_text())
    nonempty(decision, ["maintainer", "knowledge_version"])
    utc(decision["created_at"])
    if (
        decision["decision"] != "release"
        or not re.fullmatch(r"\d+\.\d+\.\d+", decision["knowledge_version"])
        or decision["engine_compatibility"] != ["0.0.0"]
    ):
        raise ValueError("decisão ou combinação Research inválida")
    evidence(decision_file.parent, decision)
    selected = decision["records"]
    if not isinstance(selected, list) or not selected:
        raise ValueError("seleção vazia")
    catalog = {
        k: [] for k in ("sources", "artifacts", "rights", "activities", "reviews")
    }
    rows, used, references, seen = [], set(), [], set()
    for ref in selected:
        key, rev = ref["record_id"], ref["revision"]
        if key in seen or type(rev) is not int:
            raise ValueError("seleção repetida ou revisão inválida")
        seen.add(key)
        row = db.execute(
            "select * from candidate where id=? and rev=?", (key, rev)
        ).fetchone()
        if (
            not row
            or rev
            != db.execute(
                "select max(rev) from candidate where id=?", (key,)
            ).fetchone()[0]
        ):
            raise ValueError("seleção ausente ou substituída")
        state, reviewers = review(db, row)
        if state != "accepted":
            raise ValueError(f"{key}: revisão de pares {state}")
        if not db.execute(
            "select 1 from curation where id=? and rev=?", (key, rev)
        ).fetchone():
            raise ValueError("falta decisão CURATED")
        a = source_for(db, row)
        record = describe(row, a)
        if a["hash"] not in used:
            right = decision["rights"][a["hash"]]
            nonempty(right, ["reviewer_id", "jurisdiction"])
            if (
                right["decision"] != "approved"
                or set(right["scope"]) != SCOPES
                or not isinstance(right["obligations"], list)
                or not all(isinstance(v, str) for v in right["obligations"])
            ):
                raise ValueError("permissões incompletas")
            utc(right["reviewed_at"])
            evidence(decision_file.parent, right)
            rights_id = record["rights_id"]
            catalog["rights"].append(
                {
                    k: right[k]
                    for k in (
                        "decision",
                        "reviewer_id",
                        "jurisdiction",
                        "scope",
                        "reviewed_at",
                        "obligations",
                        "evidence_locator",
                    )
                }
                | {"rights_id": rights_id}
            )
            if not any(s["source_id"] == a["source"] for s in catalog["sources"]):
                catalog["sources"].append(
                    {
                        "source_id": a["source"],
                        "source_type": "synthetic",
                        "title": f"dlg-pilot-001/{a['source']}",
                        "creator": a["creator"],
                        "source_locator": f"pilot/{a['source']}.jsonl",
                        "checked_at": a["acquired"],
                    }
                )
            catalog["artifacts"].append(
                {
                    "artifact_id": a["hash"],
                    "source_id": a["source"],
                    "media_type": "application/x-ndjson",
                    "byte_length": len(a["original"]),
                    "sha256": a["hash"],
                    "storage_locator": f"editorial:sha256:{a['hash']}",
                    "acquired_at": a["acquired"],
                    "rights_id": rights_id,
                }
            )
            used.add(a["hash"])
        catalog["activities"].append(
            {
                "activity_id": record["provenance"]["activity_ids"][0],
                "input_ids": [a["hash"]],
                "output_ids": [f"{key}@{rev}"],
                "operation": "parse_jsonl",
                "tool_version": "0.0.0",
                "config_digest": digest(encode({"schema": SCHEMA})),
                "agent_id": "mkb.prepare",
                "occurred_at": a["acquired"],
            }
        )
        catalog["reviews"].append(
            {
                "record_id": key,
                "revision": rev,
                "reviewer_ids": reviewers,
                "decision": "approved",
            }
        )
        record["status"] = "RELEASED"
        rows.append(record)
        references.append({"record_id": key, "revision": rev})
    files = {
        "records.jsonl": b"".join(
            encode(r) + b"\n" for r in sorted(rows, key=lambda r: r["record_id"])
        ),
        "catalog.json": encode(catalog),
    }
    manifest = {
        "knowledge_version": decision["knowledge_version"],
        "schema_version": SCHEMA,
        "engine_compatibility": decision["engine_compatibility"],
        "created_at": decision["created_at"],
        "build_profile": PROFILE,
        "records": references,
        "rights_summary": [r["rights_id"] for r in catalog["rights"]],
        "artifacts": [
            {"path": k, "byte_length": len(v), "sha256": digest(v)}
            for k, v in files.items()
        ],
    }
    files["manifest.json"] = encode(manifest)
    fingerprint = digest(files["manifest.json"])
    declaration = digest(encode(decision))
    previous = db.execute(
        "select manifest_sha256,decision_sha256 from edition where version=?",
        (decision["knowledge_version"],),
    ).fetchone()
    if previous and tuple(previous) != (fingerprint, declaration):
        raise ValueError("versão da edição já reservada para conteúdo diferente")
    if destination.exists():
        if {p.name for p in destination.iterdir()} != set(files) or any(
            (destination / k).read_bytes() != v for k, v in files.items()
        ):
            raise ValueError("destino já contém outra edição")
    else:
        _write_package(destination, files)
    db.execute(
        "insert or ignore into edition values(?,?,?,?)",
        (
            decision["knowledge_version"],
            fingerprint,
            declaration,
            files["manifest.json"],
        ),
    )
    return fingerprint


def _write_package(destination, files):
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(dir=destination.parent))
    try:
        for k, v in files.items():
            (tmp / k).write_bytes(v)
        os.rename(tmp, destination)
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)
