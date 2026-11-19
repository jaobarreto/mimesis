"""Pacotes inteiramente sintéticos construídos somente no diretório temporário."""

import json
import sqlite3
import subprocess
import sys
from contextlib import closing
from copy import deepcopy

import pytest

from research_compiler.contract import OPERATIONS, canonical, sha
from research_compiler.projection import compile_package

WHEN = "2026-11-19T00:00:00Z"


def documents():
    record = {
        "record_id": "t1",
        "revision": 1,
        "language": "pt-BR",
        "domain": "MKB-DLG",
        "schema_version": "0.1.0",
        "status": "RELEASED",
        "source_id": "s",
        "rights_id": "r",
        "provenance": {"artifact_id": "raw", "locator": "line:1", "activity_ids": ["ev"]},
        "payload": {
            "prompts": [{"prompt_id": "p", "text": "  VOCÊ   vem? "}],
            "responses": [{"response_id": "a", "text": "Sim."}],
        },
    }
    catalog = {
        "sources": [
            {
                "source_id": "s",
                "source_type": "fixture",
                "title": "Teste",
                "creator": "fixture",
                "source_locator": "private:test",
                "checked_at": WHEN,
            }
        ],
        "artifacts": [
            {
                "artifact_id": "raw",
                "source_id": "s",
                "media_type": "application/x-ndjson",
                "byte_length": 2,
                "sha256": sha(b"{}"),
                "storage_locator": "private:raw",
                "acquired_at": WHEN,
                "rights_id": "r",
            }
        ],
        "rights": [
            {
                "rights_id": "r",
                "evidence_locator": "private:decision",
                "scope": sorted(OPERATIONS),
                "jurisdiction": "BR",
                "decision": "approved",
                "reviewer_id": "review-rights",
                "reviewed_at": WHEN,
                "obligations": [],
            }
        ],
        "activities": [
            {
                "activity_id": "ev",
                "input_ids": ["raw"],
                "output_ids": ["t1@1"],
                "operation": "curate",
                "tool_version": "1",
                "config_digest": sha(b"test"),
                "agent_id": "fixture",
                "occurred_at": WHEN,
            }
        ],
        "reviews": [
            {
                "record_id": "t1",
                "revision": 1,
                "reviewer_ids": ["first", "second"],
                "decision": "approved",
            }
        ],
    }
    manifest = {
        "knowledge_version": "0.0.1",
        "schema_version": "0.1.0",
        "build_profile": "research-dlg-v1",
        "created_at": WHEN,
        "engine_compatibility": ["0.0.0"],
        "rights_summary": ["r"],
        "records": [{"record_id": "t1", "revision": 1}],
    }
    return record, catalog, manifest


def write(package, records, catalog, manifest):
    package.mkdir(exist_ok=True)
    data = {
        "records.jsonl": b"".join(canonical(r) + b"\n" for r in records),
        "catalog.json": canonical(catalog),
    }
    manifest["artifacts"] = []
    for name, content in data.items():
        (package / name).write_bytes(content)
        manifest["artifacts"].append(
            {"path": name, "sha256": sha(content), "byte_length": len(content)}
        )
    content = canonical(manifest)
    (package / "manifest.json").write_bytes(content)
    return sha(content)


def test_rebuild_and_trace(tmp_path):
    record, catalog, manifest = documents()
    package = tmp_path / "pkg"
    pin = write(package, [record], catalog, manifest)
    first, second = (tmp_path / name for name in ("a.sqlite", "b.sqlite"))
    cmd = [
        sys.executable,
        "-m",
        "research_compiler",
        str(package),
        str(first),
        "--manifest-sha256",
        pin,
    ]
    receipt = json.loads(subprocess.run(cmd, capture_output=True, check=True).stdout)
    assert receipt == compile_package(package, second, pin)
    assert receipt["sqlite_sha256"] == sha(second.read_bytes())
    assert first.read_bytes() == second.read_bytes()
    assert receipt["talksets"] == receipt["prompts"] == receipt["responses"] == 1
    with closing(sqlite3.connect(first)) as db:
        assert db.execute(
            "select normalized_text from prompt_fts where prompt_fts match 'você'"
        ).fetchone() == ("você vem?",)
        assert db.execute("select text from prompt").fetchone() == ("  VOCÊ   vem? ",)
        assert db.execute(
            "select revision,artifact_id,locator,rights_id from response join talkset using(talkset_id) where response_id='a'"
        ).fetchone() == (1, "raw", "line:1", "r")
        assert dict(db.execute("select * from build_info"))["manifest_sha256"] == pin


@pytest.mark.parametrize(
    "mutate",
    [
        lambda r, c, m: r.update(status="PROCESSED"),
        lambda r, c, m: r.update(revision=True),
        lambda r, c, m: r.update(language="pt"),
        lambda r, c, m: r["payload"].update(context={"required": True}),
        lambda r, c, m: r["payload"]["prompts"][0].update(text=" "),
        lambda r, c, m: r["payload"].update(responses=[]),
        lambda r, c, m: r["provenance"].update(locator=""),
        lambda r, c, m: r["provenance"].update(artifact_id="../raw"),
        lambda r, c, m: c["activities"][0].update(input_ids=["wrong"]),
        lambda r, c, m: c["activities"][0].update(output_ids=["t1@2"]),
        lambda r, c, m: c["rights"][0].update(decision="pending"),
        lambda r, c, m: c["rights"][0].update(evidence_locator=None),
        lambda r, c, m: c["rights"][0].update(scope=["access"]),
        lambda r, c, m: c["reviews"][0].update(reviewer_ids=["same", "same"]),
        lambda r, c, m: c["reviews"][0].update(revision=2),
        lambda r, c, m: m.update(records=[]),
        lambda r, c, m: m.update(engine_compatibility=["0.0.1"]),
        lambda r, c, m: m.update(schema_version="0.1.1"),
        lambda r, c, m: m.update(rights_summary=["unknown"]),
    ],
)
def test_reject_invalid_package(tmp_path, mutate):
    record, catalog, manifest = documents()
    mutate(record, catalog, manifest)
    package, active = tmp_path / "pkg", tmp_path / "active.sqlite"
    pin = write(package, [record], catalog, manifest)
    active.write_bytes(b"anterior")
    with pytest.raises(ValueError):
        compile_package(package, active, pin)
    assert active.read_bytes() == b"anterior"


@pytest.mark.parametrize("name", ["manifest.json", "catalog.json", "records.jsonl"])
def test_digest_mismatch(tmp_path, name):
    package = tmp_path / "pkg"
    record, catalog, manifest = documents()
    pin = write(package, [record], catalog, manifest)
    with (package / name).open("ab") as data:
        data.write(b" ")
    with pytest.raises(ValueError, match="SHA-256"):
        compile_package(package, tmp_path / "out.sqlite", pin)


def test_sql_failure_preserves_active_index(tmp_path):
    package, active = tmp_path / "pkg", tmp_path / "active.sqlite"
    record, catalog, manifest = documents()
    compile_package(package, active, write(package, [record], catalog, manifest))
    previous = active.read_bytes()
    other = deepcopy(record)
    other["record_id"] = "t2"
    manifest["records"].append({"record_id": "t2", "revision": 1})
    catalog["reviews"].append(dict(catalog["reviews"][0], record_id="t2"))
    catalog["activities"][0]["output_ids"].append("t2@1")
    pin = write(package, [record, other], catalog, manifest)
    with pytest.raises(sqlite3.IntegrityError, match="prompt.prompt_id"):
        compile_package(package, active, pin)
    assert active.read_bytes() == previous
    assert not list(tmp_path.glob(".mimesis-*"))


def test_duplicate_json_keys_are_rejected(tmp_path):
    record, catalog, manifest = documents()
    package = tmp_path / "pkg"
    write(package, [record], catalog, manifest)
    path = package / "manifest.json"
    data = b'{"schema_version":"0.1.0",' + path.read_bytes()[1:]
    path.write_bytes(data)
    with pytest.raises(ValueError, match="repetida"):
        compile_package(package, tmp_path / "out.sqlite", sha(data))


@pytest.mark.parametrize("step", [0, 1])
def test_all_activity_inputs_must_resolve_at_each_step(tmp_path, step):
    record, catalog, manifest = documents()
    first = catalog["activities"][0]
    first["output_ids"] = ["transcript"]
    second = dict(first, activity_id="review", input_ids=["transcript"], output_ids=["t1@1"])
    catalog["activities"].append(second)
    record["provenance"]["activity_ids"].append("review")
    package = tmp_path / "pkg"
    active = tmp_path / "active.sqlite"
    compile_package(package, active, write(package, [record], catalog, manifest))
    before = active.read_bytes()

    catalog["activities"][step]["input_ids"].append("unresolved")
    pin = write(package, [record], catalog, manifest)
    with pytest.raises(ValueError, match="entrada de atividade desconectada"):
        compile_package(package, active, pin)
    assert active.read_bytes() == before
