"""Consulta experimental sobre uma projeção de fixtures em memória."""

import json
import re
import sqlite3
from contextlib import ExitStack
from dataclasses import asdict
from time import perf_counter_ns

from research_compiler.contract import canonical, sha
from research_compiler.projection import CONFIG, TOKENIZER, create_projection, normalize

from .fixtures import EDITION, ROWS, records
from .retrieval import RETRIEVERS

POLICY = "fixture-ranking-v1"
MAX_LENGTH = 512
NEGATION = {"não", "nao", "nunca", "jamais", "nem", "sem"}
ROLE = {"eu": 1, "me": 1, "mim": 1, "você": 2, "voce": 2, "te": 2, "ti": 2}
# Minimum and ambiguity margin, separately for each method.
LIMITS = {"exact": (1, 0), "fuzzy": (0.79, 0.04), "levenshtein": (0.73, 0.04), "bm25": (0.6, 0.12)}
FALLBACK = "Você pode reformular?"


def guard(query, prompt):
    left, right = (re.findall(r"[^\W_]+", value) for value in (query, prompt))
    if bool(NEGATION.intersection(left)) != bool(NEGATION.intersection(right)):
        return "negation_mismatch"
    orientations = []
    for words in (left, right):
        orientations.append(list(dict.fromkeys(ROLE[w] for w in words if w in ROLE)))
    first, second = orientations
    if len(first) == len(second) == 2 and first != second:
        return "role_order_mismatch"
    return None


class Experiment:
    def __enter__(self):
        with ExitStack() as cleanup:
            self.db = sqlite3.connect(":memory:")
            cleanup.callback(self.db.close)
            self.tokenizer = sqlite3.connect(":memory:")
            cleanup.callback(self.tokenizer.close)
            knowledge = records()
            self.info = {
                "mode": "experimental_fixture",
                "fixture": EDITION,
                "fixture_sha256": sha(canonical(ROWS)),
                "config_sha256": sha(canonical(CONFIG)),
                "sqlite_version": sqlite3.sqlite_version,
            }
            create_projection(self.db, knowledge, self.info)
            self.db.executescript("""
                CREATE VIRTUAL TABLE prompt_vocab USING fts5vocab(prompt_fts,'instance');
                PRAGMA query_only=ON;
            """)
            self.tokenizer.executescript(f"""
                CREATE VIRTUAL TABLE query_tokens USING fts5(text, tokenize='{TOKENIZER}');
                CREATE VIRTUAL TABLE query_vocab USING fts5vocab(query_tokens,'row');
            """)
            self.cleanup = cleanup.pop_all()
        return self

    def __exit__(self, *exc):
        self.cleanup.close()

    def query(self, text, method, *, language="pt-BR"):
        start = perf_counter_ns()
        retrieve = RETRIEVERS[method]
        minimum, margin = LIMITS[method]
        trace = {
            "mode": "experimental_fixture",
            "algorithm": method,
            "policy": POLICY,
            "original_input": text,
            "language": language,
            "normalized_input": None,
            "tokens": [],
            "projection": self.info.copy(),
            "minimum": minimum,
            "minimum_on": "coverage" if method == "bm25" else "score",
            "margin": margin,
            "margin_on": "relative_score" if method == "bm25" else "score",
            "candidates": [],
            "response_ranking": [],
            "selected": None,
        }

        def result(outcome, reason, response=None):
            trace["elapsed_ms"] = (perf_counter_ns() - start) / 1_000_000
            return {"outcome": outcome, "reason": reason, "text": response, "trace": trace}

        if (
            not isinstance(text, str)
            or language != "pt-BR"
            or len(text) > MAX_LENGTH
            or any(0xD800 <= ord(c) <= 0xDFFF or c == "\x00" for c in text)
        ):
            return result("invalid_input", "invalid_text_or_language")
        key = normalize(text)
        trace["normalized_input"] = key
        if not key:
            return result("invalid_input", "blank_text")

        with self.tokenizer:
            self.tokenizer.execute("DELETE FROM query_tokens")
            self.tokenizer.execute("INSERT INTO query_tokens VALUES (?)", (key,))
            terms = {row[0] for row in self.tokenizer.execute("SELECT term FROM query_vocab")}
        trace["tokens"] = sorted(terms)
        hits = sorted(
            retrieve(self.db, key, terms),
            key=lambda hit: (-hit.score, hit.talkset_id, hit.prompt_id),
        )
        groups = {}
        for hit in hits:
            blocked = guard(key, hit.key)
            trace["candidates"].append(asdict(hit) | {"filter": blocked})
            if blocked is None:
                groups.setdefault(hit.talkset_id, hit)
        ranked = list(groups.values())
        for hit in ranked:
            trace["response_ranking"].extend(
                {"talkset_id": hit.talkset_id, "response_id": row[0], "score": hit.score}
                for row in self.db.execute(
                    "SELECT response_id FROM response WHERE talkset_id=? ORDER BY response_id",
                    (hit.talkset_id,),
                )
            )
        if not ranked:
            return result("fallback", "filtered" if hits else "no_match", FALLBACK)
        best = ranked[0]
        quality = best.coverage if method == "bm25" else best.score
        if quality < minimum:
            return result("fallback", "low_score", FALLBACK)
        if len(ranked) > 1:
            rival = ranked[1]
            gap = best.score - rival.score
            if method == "bm25" and best.score:
                gap /= best.score
            trace["observed_margin"] = gap
            if gap == 0 or gap < margin:
                return result("fallback", "ambiguous", FALLBACK)

        row = self.db.execute(
            """
            SELECT r.response_id,r.text,t.revision,t.source_id,t.rights_id,
                   t.artifact_id,t.locator,t.activity_ids
            FROM response AS r JOIN talkset AS t USING(talkset_id)
            WHERE r.talkset_id=? ORDER BY r.response_id LIMIT 1
        """,
            (best.talkset_id,),
        ).fetchone()
        if row is None:
            raise sqlite3.DatabaseError("Talkset experimental sem resposta")
        rid, response, revision, source, rights, artifact, locator, activities = row
        trace["selected"] = {
            "talkset_id": best.talkset_id,
            "prompt_id": best.prompt_id,
            "response_id": rid,
            "revision": revision,
            "source_id": source,
            "rights_id": rights,
            "artifact_id": artifact,
            "locator": locator,
            "activity_ids": json.loads(activities),
        }
        return result("answered", "matched", response)
