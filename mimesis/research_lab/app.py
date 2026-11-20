import json
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from research_experiment.engine import Experiment
from research_lab.performance import SIZES
from research_lab.study import METHODS, benchmark


def table(rows):
    if rows:
        st.dataframe(pd.DataFrame(rows), hide_index=True)
    else:
        st.caption("Nenhum registro.")


def inspector(result):
    tr = result["trace"]
    st.write("Texto original")
    st.text(tr["original_input"])
    st.write("Texto normalizado", tr["normalized_input"])
    st.write("Tokens distintos em ordem lexical", tr["tokens"])
    st.caption(METHODS[tr["algorithm"]][1])
    st.json(
        {k: tr[k] for k in ("policy", "minimum", "minimum_on", "margin", "margin_on")}
        | {"observed_margin": tr.get("observed_margin")}
    )
    st.write("Ranking de entradas")
    st.caption(
        "Ordem por escore dentro do método, depois por IDs de Talkset e entrada. O campo filter indica bloqueios por negação ou ordem dos papéis."
    )
    table(tr["candidates"])
    st.write("Respostas elegíveis antes do mínimo e da margem")
    st.caption(
        "Cada família usa sua melhor entrada. Empate entre famílias produz abstenção. Dentro da família, vence o menor ID de resposta."
    )
    table(tr["response_ranking"])
    st.write("Decisão", result["reason"])
    st.write("Resposta selecionada", result["text"] if tr["selected"] else "Nenhuma")
    st.write("Procedência", tr["selected"])
    st.json(tr["projection"], expanded=False)
    st.caption(f"Consulta em {tr['elapsed_ms']:.3f} ms")


def playground(engine):
    method = st.selectbox("Recuperador", list(METHODS), format_func=lambda k: METHODS[k][0])
    history = st.session_state.setdefault("history", [])
    st.caption(
        "O histórico guarda os últimos 50 envios nesta sessão. O motor recebe somente a consulta atual."
    )
    if st.button("Limpar histórico"):
        history.clear()
    query = st.chat_input("Enviar consulta experimental", max_chars=512)
    if query:
        history.append(engine.query(query, method))
        del history[:-50]
    for result in history:
        trace = result["trace"]
        with st.chat_message("user"):
            st.text(trace["original_input"])
        with st.chat_message("assistant"):
            st.text(result["text"] or result["reason"])
            st.caption(f"{METHODS[trace['algorithm']][0]} · {result['reason']}")
            with st.expander("Inspector"):
                inspector(result)


def comparison(engine):
    with st.form("comparison_query"):
        query = st.text_input("Consulta comum", value="Posso fechr a janela?", max_chars=512)
        run = st.form_submit_button("Comparar métodos")
    if run:
        st.session_state.comparison = {key: engine.query(query, key) for key in METHODS}
    results = st.session_state.get("comparison", {})
    if results:
        st.text(next(iter(results.values()))["trace"]["original_input"])
        for column, (method, result) in zip(st.columns(4), results.items()):
            with column:
                st.subheader(METHODS[method][0])
                st.text(result["text"] or result["reason"])
                st.caption(result["reason"])
                with st.expander("Inspector"):
                    inspector(result)


def explorer(engine):
    def read(sql, params=()):
        return pd.read_sql_query(sql, engine.db, params=params)

    st.caption(
        f"{engine.info['fixture']} · {engine.info['talksets']} Talksets · {engine.info['prompts']} entradas · {engine.info['responses']} respostas"
    )
    key = st.selectbox(
        "Talkset carregado", read("SELECT talkset_id FROM talkset ORDER BY 1").talkset_id.tolist()
    )
    st.json(read("SELECT * FROM talkset WHERE talkset_id=?", (key,)).iloc[0].to_dict())
    st.write("Entradas")
    st.dataframe(
        read("SELECT * FROM prompt WHERE talkset_id=? ORDER BY prompt_id", (key,)), hide_index=True
    )
    st.write("Respostas")
    st.dataframe(
        read("SELECT * FROM response WHERE talkset_id=? ORDER BY response_id", (key,)),
        hide_index=True,
    )


def bench(engine):
    st.caption(
        "Suite técnica v1. Cada método executa cinco casos com expectativa sintética e uma sondagem sem julgamento. Respostas incorretas incluem falsas aceitações."
    )
    if st.button("Executar consultas"):
        st.session_state.bench = benchmark(engine)
    rows = st.session_state.get("bench", [])
    if rows:
        summaries = []
        for method in METHODS:
            subset = [r for r in rows if r["method"] == method]
            judged = [r for r in subset if r["expected"] is not None]
            summaries.append(
                {
                    "método": method,
                    "consultas": len(subset),
                    "com expectativa": len(judged),
                    "corretas": sum(r["correct_answer"] for r in judged),
                    "incorretas": sum(r["wrong_answer"] for r in judged),
                    "falsas aceitações": sum(r["false_accept"] for r in judged),
                    "abstenções": sum(r["outcome"] == "fallback" for r in subset),
                    "mediana (ms)": np.median([r["elapsed_ms"] for r in subset]),
                }
            )
        table(summaries)
        index = st.selectbox(
            "Consulta e ranking",
            range(len(rows)),
            format_func=lambda i: f"{rows[i]['method']} · {rows[i]['query']}",
        )
        st.json(rows[index])


def performance():
    size = st.selectbox("Talksets sintéticos por processo", SIZES)
    st.caption(
        "Cada registro de carga tem uma entrada e uma resposta. A latência mede 25 buscas exatas indexadas. A construção inclui índices e verificação de integridade. RSS mede o pico do processo Linux em KiB."
    )
    results = st.session_state.setdefault("measurements", [])
    if st.button("Medir carga"):
        with st.spinner("Construindo a projeção em memória…"):
            try:
                proc = subprocess.run(
                    [sys.executable, "-m", "research_lab.performance", "--size", str(size)],
                    cwd=Path(__file__).resolve().parents[1],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=300,
                )
                results.append(json.loads(proc.stdout))
            except (subprocess.SubprocessError, ValueError, OSError) as error:
                st.error(f"Ensaio interrompido: {error}")
    if results:
        table(
            [
                {
                    k: r[k]
                    for k in (
                        "records",
                        "build_with_indexes_ms",
                        "fts_rebuild_ms",
                        "core_init_ms",
                        "load_ready_ms",
                        "cpu_ms",
                        "peak_rss_kib",
                        "sqlite_disk_bytes",
                        "sqlite_logical_bytes",
                    )
                }
                | {"exact_p95_ms": np.percentile(r["exact_lookup_ms"], 95)}
                for r in results
            ]
        )
        fig, ax = plt.subplots()
        ax.scatter([r["records"] for r in results], [r["load_ready_ms"] for r in results])
        ax.set(xscale="log", xlabel="Talksets", ylabel="Preparação da carga (ms)")
        st.pyplot(fig)
        plt.close(fig)


def main():
    st.set_page_config(page_title="MIMESIS Lab", layout="wide")
    st.title("MIMESIS Lab")
    st.caption("0.0.0 · Research · Laboratório local")
    if not st.sidebar.checkbox("Ativar fixtures sintéticas"):
        st.info("Ative as fixtures para iniciar o experimento em memória.")
        return
    pages = {
        "Playground": playground,
        "Comparação": comparison,
        "Knowledge Explorer": explorer,
        "Benchmark Lab": bench,
    }
    page = st.sidebar.radio("Ambiente", [*pages, "Performance Lab"])
    st.header(page)
    if page == "Performance Lab":
        performance()
    else:
        with Experiment() as engine:
            pages[page](engine)


main()
