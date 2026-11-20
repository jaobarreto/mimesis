from pathlib import Path

import pytest

from research_experiment.engine import Experiment
from research_lab.performance import measure
from research_lab.study import benchmark

ROOT = Path(__file__).resolve().parents[1]


def test_technical_oracle_and_ranks():
    with Experiment() as engine:
        rows = benchmark(engine)
        ranks = {
            key: [
                hit["prompt_id"]
                for hit in engine.query("A janela está pronta?", key)["trace"]["candidates"]
            ]
            for key in ("fuzzy", "levenshtein")
        }
    assert ranks["fuzzy"][2] == "window-p1" and ranks["levenshtein"][2] == "window-p2"
    assert len(rows) == 24
    for row in rows:
        if row["case"] == "literal":
            assert row["correct_answer"] and row["ranking"]
        if row["case"] == "exploratória":
            assert all(
                row[k] is None
                for k in ("expected", "correct_answer", "wrong_answer", "false_accept")
            )


def test_load_scope_and_storage():
    with pytest.raises(ValueError):
        measure(101)
    result = measure(100)
    assert len(result["exact_lookup_ms"]) == 25
    assert result["sqlite_logical_bytes"] > 0 and result["sqlite_disk_bytes"] == 0
    assert result["fts_rebuild_ms"] > 0


def test_streamlit_session_and_views():
    testing = pytest.importorskip("streamlit.testing.v1")
    app = testing.AppTest.from_file(str(ROOT / "research_lab/app.py"), default_timeout=30).run()
    assert not app.chat_input
    app.checkbox[0].check().run()
    app.chat_input[0].set_value("A luz está pronta?").run()
    app.chat_input[0].set_value("Posso fechar a janela?").run()
    assert [r["reason"] for r in app.session_state["history"]] == ["ambiguous", "matched"]
    assert not app.exception
    app.radio[0].set_value("Comparação").run()
    app.button[0].click().run()
    assert len(app.session_state["comparison"]) == 4 and not app.exception
    app.radio[0].set_value("Knowledge Explorer").run()
    app.selectbox[0].set_value("window").run()
    assert len(app.dataframe[0].value) == 2 and not app.exception
    app.radio[0].set_value("Benchmark Lab").run()
    app.button[0].click().run()
    assert len(app.session_state["bench"]) == 24 and not app.exception
    app.radio[0].set_value("Performance Lab").run()
    app.button[0].click().run()
    assert app.session_state["measurements"][0]["records"] == 100 and not app.exception
