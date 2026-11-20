"""Recuperadores isolados, com escore nativo e orientação explícita."""

from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass(frozen=True)
class Hit:
    prompt_id: str
    talkset_id: str
    key: str
    raw_score: float
    score: float
    coverage: float | None = None


def exact(db, key, terms):
    rows = db.execute(
        "SELECT prompt_id, talkset_id, normalized_text FROM prompt WHERE normalized_text=?",
        (key,),
    )
    return [Hit(*row, 1, 1) for row in rows]


def scan(db, key, scorer):
    return [
        Hit(*row, *scorer(key, row[2]))
        for row in db.execute("SELECT prompt_id,talkset_id,normalized_text FROM prompt")
    ]


def fuzzy(db, key, terms):
    def score(a, b):
        # SequenceMatcher may be asymmetric when matching blocks tie.
        ratio = (
            SequenceMatcher(None, a, b, autojunk=False).ratio()
            + SequenceMatcher(None, b, a, autojunk=False).ratio()
        ) / 2
        return ratio, ratio

    return scan(db, key, score)


def distance(a, b):
    previous = list(range(len(b) + 1))
    for index, left in enumerate(a, 1):
        current = [index]
        for column, right in enumerate(b, 1):
            current.append(
                min(
                    previous[column] + 1,
                    current[-1] + 1,
                    previous[column - 1] + (left != right),
                )
            )
        previous = current
    return previous[-1]


def levenshtein(db, key, terms):
    def score(a, b):
        edits = distance(a, b)
        return edits, 1 - edits / max(len(a), len(b))

    return scan(db, key, score)


def bm25(db, key, terms):
    if not terms:
        return []
    # MATCH interprets SQL parameters as an FTS expression. Quote each literal.
    expression = " OR ".join('"' + term.replace('"', '""') + '"' for term in sorted(terms))
    rows = db.execute(
        """
        SELECT p.prompt_id,p.talkset_id,p.normalized_text,bm25(prompt_fts),p.rowid
        FROM prompt_fts JOIN prompt AS p ON p.rowid=prompt_fts.rowid
        WHERE prompt_fts MATCH ?
    """,
        (expression,),
    )
    return [
        Hit(
            pid,
            tid,
            text,
            raw,
            -raw,
            len(
                terms.intersection(
                    t[0] for t in db.execute("SELECT term FROM prompt_vocab WHERE doc=?", (rowid,))
                )
            )
            / len(terms),
        )
        for pid, tid, text, raw, rowid in rows
    ]


RETRIEVERS = {"exact": exact, "fuzzy": fuzzy, "levenshtein": levenshtein, "bm25": bm25}
