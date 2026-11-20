"""Catálogos administrativos do lote sintético em processamento."""

from .pilot import Candidate, digest, encode, read_json
from .release import SCHEMA, describe, source_for


def inventory(db):
    sources, artifacts, rights, activities, events = {}, [], [], [], []
    for a in db.execute("select * from artifact order by source,acquired,hash"):
        sha, source, at = a["hash"], a["source"], a["acquired"]
        if digest(a["original"]) != sha:
            raise ValueError("bytes originais alterados")
        sources.setdefault(
            source,
            {
                "source_id": source,
                "source_type": "synthetic",
                "title": f"dlg-pilot-001/{source}",
                "creator": a["creator"],
                "source_locator": f"pilot/{source}.jsonl",
                "checked_at": at,
            },
        )
        rid = f"rights-{sha}"
        artifacts.append(
            {
                "artifact_id": sha,
                "source_id": source,
                "media_type": "application/x-ndjson",
                "sha256": sha,
                "byte_length": len(a["original"]),
                "rights_id": rid,
                "storage_locator": f"editorial:sha256:{sha}",
                "acquired_at": at,
            }
        )
        rights.append(
            {
                "rights_id": rid,
                "evidence_locator": "pilot/README.md",
                "scope": {
                    "synthetic_candidate_preparation": "allowed",
                    "incorporation": "unresolved",
                    "local_query": "unresolved",
                    "redistribution": "unresolved",
                },
                "decision": "pending",
                "jurisdiction": None,
                "reviewer_id": None,
                "reviewed_at": None,
                "obligations": None,
            }
        )
        events.append(
            {
                "event_id": f"raw-{sha}",
                "artifact_id": sha,
                "from_state": None,
                "to_state": "RAW",
                "agent_id": "mkb.prepare",
                "occurred_at": at,
                "reason": "recebimento local de candidato sintético",
            }
        )
    for row in db.execute("select * from candidate order by id,rev"):
        a = source_for(db, row)
        r = Candidate.model_validate_json(row["data"])
        identity = {"record_id": r.id, "revision": r.revision}
        activity_id = describe(row, a)["provenance"]["activity_ids"][0]
        activities.append(
            {
                "activity_id": activity_id,
                "input_ids": [a["hash"]],
                "output_ids": [f"{r.id}@{r.revision}"],
                "operation": "parse_jsonl",
                "tool_version": "0.0.0",
                "config_digest": digest(encode({"schema": SCHEMA})),
                "agent_id": "mkb.prepare",
                "occurred_at": a["acquired"],
            }
        )
        events.append(
            {
                **identity,
                "event_id": f"processed-{r.id}-{r.revision}",
                "from_state": "RAW",
                "to_state": "PROCESSED",
                "occurred_at": a["acquired"],
                "reason": "esquema do candidato validado",
                "agent_id": "mkb.prepare",
            }
        )
    return {
        "purpose": "initial_processing",
        "sources": list(sources.values()),
        "artifacts": artifacts,
        "rights": rights,
        "activities": activities,
        "events": events,
        "curation_decisions": [
            read_json(r[0])
            for r in db.execute("select decision from curation order by id,rev")
        ],
    }


def write(db, path):
    content = encode(inventory(db)) + b"\n"
    with path.open("xb") as stream:
        stream.write(content)
