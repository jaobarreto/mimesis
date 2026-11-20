"""Protocolo técnico core-diagnostics-v1."""

import argparse
import json

from research_experiment.engine import LIMITS, POLICY, Experiment
from research_experiment.retrieval import RETRIEVERS

METHODS = {
    "exact": (
        "Exact Matching",
        "Igualdade entre chaves normalizadas. O índice de igualdade recupera entradas com escore 1.",
    ),
    "fuzzy": (
        "Fuzzy Matching",
        "Média de 2M/(|a|+|b|) nas duas direções. M soma os blocos coincidentes de SequenceMatcher, com autojunk desativado.",
    ),
    "levenshtein": (
        "Levenshtein Distance",
        "d conta inserções, remoções e substituições unitárias. O ranking usa 1 − d/max(|a|,|b|).",
    ),
    "bm25": (
        "BM25",
        "O FTS5 soma IDF × f × 2,2 / (f + 1,2 × (0,25 + 0,75 × |D|/avgdl)) para os termos distintos. O motor ordena por −bm25(). O mínimo usa cobertura e a margem é relativa.",
    ),
}
# Tupla vazia exige abstenção. None indica uma sondagem sem julgamento.
CASES = (
    ("literal", "Posso fechar a janela?", ("window-r1", "window-r2")),
    ("grafia", "Posso fechr a janela?", ("window-r1", "window-r2")),
    ("ambiguidade", "A luz está pronta?", ()),
    ("desconhecida", "Quantos planetas orbitam Júpiter?", ()),
    ("inversão", "Você pode embrulhar a caixa para mim?", ()),
    ("exploratória", "Uma janela aberta ajuda?", None),
)


def benchmark(engine):
    rows = []
    for i, (case, query, expected) in enumerate(CASES):
        methods = list(RETRIEVERS)
        for method in methods[i % len(methods) :] + methods[: i % len(methods)]:
            result = engine.query(query, method)
            trace = result["trace"]
            selected = trace["selected"]
            answer = selected["response_id"] if selected else None
            rows.append(
                {
                    "case": case,
                    "method": method,
                    "query": query,
                    "expected": expected,
                    "answer": answer,
                    "outcome": result["outcome"],
                    "reason": result["reason"],
                    "correct_answer": answer in expected if expected is not None else None,
                    "wrong_answer": answer is not None and answer not in expected
                    if expected is not None
                    else None,
                    "false_accept": answer is not None and expected == ()
                    if expected is not None
                    else None,
                    "elapsed_ms": trace["elapsed_ms"],
                    "ranking": trace["response_ranking"],
                    "candidates": trace["candidates"],
                }
            )
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True, action="store_true")
    parser.parse_args()
    with Experiment() as engine:
        print(
            json.dumps(
                {
                    "suite": "core-diagnostics-v1",
                    "projection": engine.info,
                    "policy": POLICY,
                    "limits": LIMITS,
                    "observations": benchmark(engine),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
