"""Fatos e pareceres abaixo existem apenas nos diretórios temporários do teste."""

import csv
import json
from pathlib import Path

import pytest

from mkb import pilot, release
from mkb.__main__ import stats

PILOT = Path(__file__).resolve().parents[1] / "pilot"


@pytest.fixture
def db(tmp_path):
    connection = pilot.connect(tmp_path / "editorial.sqlite")
    pilot.prepare(connection, PILOT)
    yield connection
    connection.close()


def ballot(db, tmp_path):
    path = tmp_path / "pairs.csv"
    pilot.sheet(db, path)
    result = []
    with path.open(newline="") as stream:
        for row in csv.DictReader(stream):
            if row["id"] == "dlg-026":
                row.update(
                    verdict="accept", reason="parecer fictício em fixture isolada"
                )
                result.append(row)
    with path.open("w", newline="") as stream:
        w = csv.DictWriter(stream, pilot.FIELDS)
        w.writeheader()
        w.writerows(result)
    return path


def decision(db, tmp_path):
    stamp = "2026-11-19T12:00:00Z"
    proof = tmp_path / "fixture.txt"
    proof.write_text("Fixture de integração, escopo exclusivo deste teste temporário.")
    ev = {
        "evidence_locator": proof.name,
        "evidence_sha256": pilot.digest(proof.read_bytes()),
    }
    sha = db.execute("select hash from candidate where id='dlg-026'").fetchone()[0]
    obj = dict(
        decision="release",
        maintainer="fixture-admin",
        knowledge_version="0.0.0",
        engine_compatibility=["0.0.0"],
        created_at=stamp,
        records=[{"record_id": "dlg-026", "revision": 1}],
        rights={
            sha: dict(
                decision="approved",
                scope=sorted(release.SCOPES),
                jurisdiction="fixture",
                reviewer_id="fixture-rights",
                reviewed_at=stamp,
                obligations=[],
                **ev,
            )
        },
        **ev,
    )
    path = tmp_path / "decision.json"
    path.write_text(json.dumps(obj))
    return path


def test_inventory_replay_and_envelopes(db, tmp_path):
    pilot.prepare(db, PILOT)
    report = stats(db)
    assert [report[k] for k in ("talksets", "prompts", "responses", "pairs")] == [
        50,
        100,
        200,
        400,
    ]
    assert report["pair_reviews"] == {"pending": 50}
    assert len(report["categories"]) == 10
    candidate = tmp_path / "processed.jsonl"
    release.candidates(db, candidate)
    rows = [json.loads(line) for line in candidate.read_text().splitlines()]
    contribution = next(r for r in rows if r["record_id"] == "dlg-026")
    assert (
        contribution["status"] == "PROCESSED"
        and contribution["source_id"] == "contribution"
    )
    assert contribution["provenance"]["locator"] == "line:1"
    assert contribution["payload"]["responses"][0]["text"] == "Claro, pode perguntar."
    assert db.execute("select count(*) from artifact").fetchone()[0] == 2


def test_gate_and_roundtrip(tmp_path):
    # Pacote de ensaio independente dos bytes e das decisões do lote em curadoria.
    data = tmp_path / "fixture"
    data.mkdir()
    for source, key in (("contribution", "dlg-026"), ("codex", "fixture-other")):
        item = {
            "id": key,
            "intent": "Greeting",
            "prompts": ["Ficha A?", "Ficha B?"],
            "responses": ["Resposta A de teste.", "Resposta B de teste."],
        }
        (data / f"{source}.jsonl").write_bytes(pilot.encode(item) + b"\n")
    db = pilot.connect(tmp_path / "fixture.sqlite")
    pilot.prepare(db, data)
    path = decision(db, tmp_path)
    output = tmp_path / "release"
    with pytest.raises(ValueError, match="pending"):
        release.export(db, path, output)
    sheet = ballot(db, tmp_path)
    for name in ("fixture-a", "fixture-a"):
        pilot.vote(db, name, sheet)
    with pytest.raises(ValueError, match="pending"):
        release.export(db, path, output)
    assert not output.exists()
    pilot.vote(db, "fixture-b", sheet)
    decision_data = json.loads(path.read_text())
    with pytest.raises(ValueError, match="CURATED"):
        release.export(db, path, output)
    cp = tmp_path / "curation.json"
    cp.write_bytes(
        pilot.encode(
            {
                "actor": "fixture-curator",
                "group_id": "fixture-origin",
                "record_id": "dlg-026",
                "artifact_sha256": next(iter(decision_data["rights"])),
                "revision": 1,
                "decision": "curate",
                "internal_research": "allowed",
                "reviewed_at": decision_data["created_at"],
                "evidence_locator": decision_data["evidence_locator"],
                "evidence_sha256": decision_data["evidence_sha256"],
            }
        )
    )
    release.curate(db, cp)
    original = path.read_bytes()
    next(iter(decision_data["rights"].values()))["scope"].remove("redistribution")
    path.write_text(json.dumps(decision_data))
    with pytest.raises(ValueError, match="permissões"):
        release.export(db, path, output)
    path.write_bytes(original)
    fingerprint = release.export(db, path, output)
    assert pilot.digest((output / "manifest.json").read_bytes()) == fingerprint
    assert release.export(db, path, output) == fingerprint
    assert stats(db)["released_revisions_ever"] == 1
    import os
    import subprocess
    import sys

    engine = os.environ.get("MIMESIS_COMPILER_DIR")
    if engine:
        receipt = subprocess.check_output(
            [
                sys.executable,
                "-m",
                "research_compiler",
                str(output),
                str(tmp_path / "index.sqlite"),
                "--manifest-sha256",
                fingerprint,
            ],
            cwd=engine,
        )
        result = json.loads(receipt)
        assert [result[k] for k in ("talksets", "prompts", "responses")] == [1, 2, 2]


def test_concurrent_votes_and_integrity(db, tmp_path):
    path = ballot(db, tmp_path)
    pilot.vote(db, "fixture-a", path)
    path.write_text(path.read_text().replace("accept", "reject"))
    with pytest.raises(ValueError, match="já registrado"):
        pilot.vote(db, "fixture-a", path)
    pilot.vote(db, "fixture-b", path)
    row = db.execute("select * from candidate where id='dlg-026'").fetchone()
    assert pilot.review(db, row)[0] == "disputed"
    with db:
        db.execute("update artifact set original=x'00' where hash=?", (row["hash"],))
    with pytest.raises(ValueError, match="alterado"):
        release.source_for(db, row)


def test_breaking_source_rolls_back(db, tmp_path):
    original = (PILOT / "codex.jsonl").read_text()
    (tmp_path / "codex.jsonl").write_text(
        original.replace("Bom dia!", "Outro texto!", 1)
    )
    (tmp_path / "contribution.jsonl").write_bytes(
        (PILOT / "contribution.jsonl").read_bytes()
    )
    with pytest.raises(ValueError, match="imutável"):
        pilot.prepare(db, tmp_path)
    assert db.execute("select count(*) from artifact").fetchone()[0] == 2
    row = json.loads(original.splitlines()[0])
    row.update(revision=2, prompts=["Texto inteiramente novo."])
    (tmp_path / "codex.jsonl").write_text(json.dumps(row) + "\n")
    pilot.prepare(db, tmp_path)
    assert (
        db.execute("select count(*) from candidate where id='dlg-001'").fetchone()[0]
        == 2
    )


@pytest.mark.parametrize("bad", ["", "   ", "x"])
def test_blank_or_duplicate_rejected(bad):
    with pytest.raises(ValueError):
        pilot.Candidate(
            id="example", intent="Greeting", prompts=["x", bad], responses=["oi"]
        )


def test_initial_provenance(db):
    from mkb.catalog import inventory

    c = inventory(db)
    assert len(c["activities"]) == 50 and len(c["events"]) == 52
    assert all(
        r["decision"] == "pending" and r["reviewer_id"] is None for r in c["rights"]
    )
    assert {a["rights_id"] for a in c["artifacts"]} == {
        r["rights_id"] for r in c["rights"]
    }
    assert {a["artifact_id"] for a in c["artifacts"]} == {
        r["input_ids"][0] for r in c["activities"]
    }
