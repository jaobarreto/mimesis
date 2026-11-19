import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from research_experiment import engine as implementation
from research_experiment.__main__ import main
from research_experiment.engine import Experiment
from research_experiment.retrieval import RETRIEVERS, distance

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def experiment():
    with Experiment() as instance:
        yield instance


@pytest.mark.parametrize("method", RETRIEVERS)
def test_known_trace(experiment, method):
    text = " POSSO  Fechar A JANELA? "
    result = experiment.query(text, method)
    assert result["outcome"] == "answered"
    trace = result["trace"]
    assert trace["original_input"] == text
    assert trace["normalized_input"] == "posso fechar a janela?"
    assert trace["tokens"] == ["a", "fechar", "janela", "posso"]
    assert trace["algorithm"] == method
    assert trace["mode"] == "experimental_fixture"
    assert trace["elapsed_ms"] >= 0
    selected = trace["selected"]
    assert selected["talkset_id"] == "window"
    assert selected["prompt_id"] == "window-p1"
    assert selected["response_id"] == "window-r1"
    assert selected["source_id"] == "synthetic-core-v1"
    assert selected["locator"] == "fixture:window"
    assert selected["revision"] == 1
    assert selected["rights_id"] == "fixture-development-only"
    assert len(selected["artifact_id"]) == 64
    assert selected["activity_ids"] == ["authored-synthetic-fixture"]
    hit = trace["candidates"][0]
    if method == "bm25":
        assert hit["score"] == -hit["raw_score"] and hit["coverage"] == 1
    else:
        assert hit["score"] == 1
        assert hit["raw_score"] == (0 if method == "levenshtein" else 1)


@pytest.mark.parametrize("method", ["fuzzy", "levenshtein", "bm25"])
def test_typo(experiment, method):
    text = "Posso fechr a janela?"
    assert experiment.query(text, "exact")["reason"] == "no_match"
    result = experiment.query(text, method)
    assert result["trace"]["selected"]["talkset_id"] == "window"
    if method == "levenshtein":
        assert result["trace"]["candidates"][0]["raw_score"] == 1


def test_distance_reference():
    assert distance("", "ação") == distance("ação", "") == 4
    assert distance("casa", "caso") == 1
    assert distance("casa", "casas") == 1
    assert distance("abcd", "abdc") == 2


def test_bm25_paraphrase_and_fts_operators(experiment):
    result = experiment.query("Podemos fazer um breve intervalo?", "bm25")
    assert result["trace"]["selected"]["talkset_id"] == "break"
    assert experiment.query('NEAR("*") AND NOT :', "bm25")["reason"] == "no_match"
    assert experiment.query("...?!", "bm25")["trace"]["tokens"] == []


def test_unicode_and_punctuation(experiment):
    result = experiment.query(" A LUZ ESTA\u0301 PRONTA? ", "exact")
    assert result["reason"] == "ambiguous"
    assert result["trace"]["normalized_input"] == "a luz está pronta?"
    assert experiment.query("A luz está pronta", "exact")["reason"] == "no_match"
    trace = experiment.query("A luz esta pronta?", "bm25")["trace"]
    assert "esta" in trace["tokens"] and "está" not in trace["tokens"]


@pytest.mark.parametrize("method", ["fuzzy", "levenshtein", "bm25"])
def test_negation_and_role_are_filtered(experiment, method):
    text = "Por favor, feche a janela."
    result = experiment.query(text, method)
    assert result["outcome"] == "fallback"
    assert any(
        hit["filter"] == "negation_mismatch" and hit["talkset_id"] == "window-open"
        for hit in result["trace"]["candidates"]
    )
    result = experiment.query("Você pode embrulhar a caixa para mim?", method)
    assert result["outcome"] == "fallback"
    assert any(
        hit["filter"] == "role_order_mismatch" and hit["talkset_id"] == "parcel"
        for hit in result["trace"]["candidates"]
    )


@pytest.mark.parametrize("method", RETRIEVERS)
def test_ambiguity_and_unknown(experiment, method):
    result = experiment.query("A luz está pronta?", method)
    assert result["reason"] == "ambiguous" and result["trace"]["selected"] is None
    assert [row["talkset_id"] for row in result["trace"]["response_ranking"][:2]] == [
        "room-light",
        "stage-light",
    ]
    assert experiment.query("Quantos planetas orbitam Júpiter?", method)["outcome"] == "fallback"


@pytest.mark.parametrize("method", RETRIEVERS)
def test_empty_knowledge(monkeypatch, method):
    monkeypatch.setattr(implementation, "records", dict)
    with Experiment() as instance:
        result = instance.query("Posso fechar a janela?", method)
    assert result["reason"] == "no_match"
    assert result["trace"]["response_ranking"] == []


def test_invalid_and_repeatability(experiment):
    for value in ("", "   ", "x" * 513, "\x00", "\ud800", None):
        assert experiment.query(value, "exact")["outcome"] == "invalid_input"
    assert experiment.query("Olá", "exact", language="en")["outcome"] == "invalid_input"
    first, second = (experiment.query("Posso fechar a janela?", "bm25") for _ in range(2))
    for result in (first, second):
        del result["trace"]["elapsed_ms"]
    assert first == second


def test_projection_integrity(experiment):
    assert experiment.db.execute("PRAGMA integrity_check").fetchall() == [("ok",)]
    assert experiment.db.execute("PRAGMA foreign_key_check").fetchall() == []
    assert experiment.info["talksets"] == 6
    assert experiment.info["prompts"] == 8
    assert experiment.info["responses"] == 7
    with pytest.raises(sqlite3.OperationalError, match="readonly"):
        experiment.db.execute("DELETE FROM prompt")


def test_cli_reports_failed_projection(monkeypatch, capsys):
    def fail(*args):
        raise sqlite3.DatabaseError("falha de teste na projeção")

    monkeypatch.setattr(implementation, "create_projection", fail)
    assert main(["--fixture", "--method", "bm25", "Olá"]) == 1
    assert json.loads(capsys.readouterr().out)["outcome"] == "unavailable"


def test_installable_zipapp_runs_outside_checkout(tmp_path):
    archive = tmp_path / "mimesis-experiment.pyz"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_experiment.py"), str(archive)],
        check=True,
        cwd=tmp_path,
    )
    command = [sys.executable, "-I", str(archive), "--method", "exact"]
    no_fixture = subprocess.run(command + ["Olá"], check=False, capture_output=True, cwd=tmp_path)
    assert no_fixture.returncode == 2 and not no_fixture.stdout
    good = subprocess.run(
        command + ["--fixture", "Posso fechar a janela?"],
        capture_output=True,
        check=True,
        cwd=tmp_path,
    )
    assert json.loads(good.stdout)["outcome"] == "answered"
    invalid = subprocess.run(
        command + ["--fixture", ""], check=False, capture_output=True, cwd=tmp_path
    )
    assert invalid.returncode == 2
    assert json.loads(invalid.stdout)["outcome"] == "invalid_input"
