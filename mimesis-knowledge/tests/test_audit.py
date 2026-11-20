import json
import shutil
from pathlib import Path

import pytest

from mkb.audit import audit

PILOT = Path(__file__).resolve().parents[1] / "pilot"


def mutate(path, i, **fields):
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    rows[i].update(fields)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


@pytest.fixture
def pilot(tmp_path):
    return Path(shutil.copytree(PILOT, tmp_path / "pilot"))


def test_exploratory_snapshot():
    report = audit(PILOT)
    assert report["status"] == "exploratory_unfrozen"
    assert report["freeze_blocked"] and not report["blocked"]
    assert report["pending_judgments"] == 33
    assert len(report["manifest_sha256"]) == 5
    assert [
        x["query"] for x in report["findings"] if x["code"] == "declared_exact"
    ] == ["q-031", "q-032", "q-033"]
    json.dumps(report, allow_nan=False)


def test_leakage_queries_responses_and_groups(pilot):
    path = pilot / "benchmark/queries.jsonl"
    mutate(path, 0, text="   BOM DIA pra Você Também ")
    mutate(path, 16, text="Bom dia pra voce tambem!", group_id="family-morning")
    report = audit(pilot)
    codes = {f["code"] for f in report["findings"] if f["level"] == "block"}
    assert (
        report["blocked"]
        and {"undeclared_exact", "cross_split_exact", "group_leakage"} <= codes
    )


def test_near_matches_prompt_review(pilot):
    mutate(pilot / "benchmark/queries.jsonl", 0, text="Posso te fazer uma pergunte?")
    report = audit(pilot)
    assert not report["blocked"]
    assert any(
        f["code"] == "near_surface" and f["target"] == "dlg-026-p1"
        for f in report["findings"]
    )
    assert any(f["code"] == "cross_split_near" for f in report["findings"])


def test_diagnostic_exception_bound_to_target(pilot):
    mutate(
        pilot / "benchmark/queries.jsonl", 30, text="Você sabe onde fica a biblioteca?"
    )
    findings = audit(pilot)["findings"]
    assert {f["code"] for f in findings if f["level"] == "block"} >= {
        "diagnostic_without_declared_exact",
        "undeclared_exact",
    }


def test_reference_class_and_identity(pilot):
    path = pilot / "benchmark/judgments.jsonl"
    mutate(
        path, 0, expected_class="ambiguous", positive_response_ids=["does-not-exist"]
    )
    mutate(path, 1, query_id="q-001")
    report = audit(pilot)
    assert report["blocked"]
    codes = {f["code"] for f in report["findings"]}
    assert {
        "unknown_response_revision",
        "class_positive_conflict",
        "duplicate_id",
        "unpaired_query_or_judgment",
    } <= codes
    assert report["manifest_sha256"] != audit(PILOT)["manifest_sha256"]
