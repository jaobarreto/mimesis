"""Auditoria reproduzível de referências e sobreposições do piloto exploratório."""

import hashlib
import re
import unicodedata
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError
from rapidfuzz.distance import Levenshtein

from .importer import strict_json_loads
from .pilot import Candidate, Text

NEAR_THRESHOLD = 0.82
DIAGNOSTICS = {
    "q-031": "dlg-026-p1",
    "q-032": "control-reverse",
    "q-033": "control-library",
}


class AuditRow(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Query(AuditRow):
    query_id: Text
    text: Text
    language: Literal["pt-BR"]
    group_id: Text
    split: Literal["dev", "test", "diagnostic"]
    scenario_id: Literal["standalone"]


class Judgment(AuditRow):
    query_id: Text
    expected_class: Literal["answerable", "unknown", "ambiguous"]
    positive_response_ids: list[Text]
    negative_response_ids: list[Text]
    rationale: Text
    revision: int = Field(ge=1)
    adjudication: Text


class Control(AuditRow):
    id: Text
    text: Text
    talkset_id: Text
    kind: Literal["near_negative", "out_of_scope"]


def lexical_key(value):
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    folded = "".join(c for c in decomposed if not unicodedata.combining(c))
    return " ".join(re.findall(r"[^\W_]+", folded))


def audit(pilot: Path) -> dict:
    pilot = Path(pilot)
    findings = []
    manifests = {}

    def flag(level, code, **evidence):
        findings.append({"level": level, "code": code, **evidence})

    def load(filename, schema):
        try:
            data = (pilot / filename).read_bytes()
            manifests[filename] = hashlib.sha256(data).hexdigest()
            lines = data.decode("utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            flag("block", "unreadable_input", file=filename, detail=str(exc))
            return []
        if not lines:
            flag("block", "empty_input", file=filename)
        rows = []
        for number, line in enumerate(lines, 1):
            try:
                rows.append(schema.model_validate(strict_json_loads(line)))
            except (ValueError, ValidationError, RecursionError) as exc:
                flag(
                    "block", "invalid_row", file=filename, line=number, detail=str(exc)
                )
        return rows

    catalog = load("codex.jsonl", Candidate) + load("contribution.jsonl", Candidate)
    controls = load("controls.jsonl", Control)
    queries = load("benchmark/queries.jsonl", Query)
    judgments = load("benchmark/judgments.jsonl", Judgment)

    def unique(ids, kind):
        for key, count in sorted(Counter(ids).items()):
            if count > 1:
                flag("block", "duplicate_id", kind=kind, id=key, count=count)

    unique((x.id for x in catalog), "talkset")
    unique((x.id for x in controls), "control")
    unique((x.query_id for x in queries), "query")
    unique((x.query_id for x in judgments), "judgment")
    talksets = {x.id for x in catalog}
    surfaces = []
    revisions = {}
    for record in catalog:
        for kind, values in [
            ("prompt", record.prompts),
            ("response", record.responses),
        ]:
            for i, text in enumerate(values, 1):
                key = f"{record.id}-{kind[0]}{i}"
                surfaces.append((key, kind, lexical_key(text)))
                if kind == "response":
                    revisions[key] = record.revision
    for control in controls:
        if control.talkset_id not in talksets:
            flag("block", "unknown_control_talkset", id=control.id)
        surfaces.append((control.id, "control", lexical_key(control.text)))
    unique((s[0] for s in surfaces), "surface")
    query_ids = {q.query_id for q in queries}
    judgment_ids = {j.query_id for j in judgments}
    for key in sorted(query_ids ^ judgment_ids):
        flag("block", "unpaired_query_or_judgment", id=key)
    for j in judgments:
        pos = set(j.positive_response_ids)
        neg = set(j.negative_response_ids)
        unique(
            j.positive_response_ids + j.negative_response_ids, f"judgment:{j.query_id}"
        )
        if (j.expected_class == "answerable") != bool(pos):
            flag("block", "class_positive_conflict", query=j.query_id)
        for ref in sorted(pos | neg):
            if revisions.get(ref) != j.revision:
                flag(
                    "block",
                    "unknown_response_revision",
                    query=j.query_id,
                    target=ref,
                    revision=j.revision,
                )

    groups = defaultdict(set)
    keys = {q.query_id: lexical_key(q.text) for q in queries}
    comparisons = Counter()
    for q in queries:
        key = keys[q.query_id]
        groups[q.group_id].add(q.split)
        if not key or not q.group_id.strip():
            flag("block", "empty_query_or_group", id=q.query_id)
        matched = False
        for target, kind, other in surfaces:
            comparisons["query_to_" + kind] += 1
            sim = Levenshtein.normalized_similarity(key, other)
            details = {
                "query": q.query_id,
                "target": target,
                "target_kind": kind,
                "split": q.split,
            }
            if sim == 1:
                allowed = (
                    q.split == "diagnostic" and DIAGNOSTICS.get(q.query_id) == target
                )
                matched |= allowed
                flag(
                    "info" if allowed else "block",
                    "declared_exact" if allowed else "undeclared_exact",
                    **details,
                )
            elif sim >= NEAR_THRESHOLD:
                flag("review", "near_surface", similarity=round(sim, 6), **details)
        if q.split == "diagnostic" and not matched:
            flag("block", "diagnostic_without_declared_exact", query=q.query_id)
    for group, splits in sorted(groups.items()):
        if len(splits) > 1:
            flag("block", "group_leakage", group=group, splits=sorted(splits))
    for q, other in combinations(queries, 2):
        if q.split == other.split:
            continue
        comparisons["cross_split_queries"] += 1
        sim = Levenshtein.normalized_similarity(keys[q.query_id], keys[other.query_id])
        if sim >= NEAR_THRESHOLD:
            flag(
                "block" if sim == 1 else "review",
                "cross_split_exact" if sim == 1 else "cross_split_near",
                query=q.query_id,
                other=other.query_id,
                similarity=round(sim, 6),
            )
    flag("review", "shared_synthetic_authorship_and_prior_catalog_exposure")
    return {
        "blocked": any(f["level"] == "block" for f in findings),
        "freeze_blocked": True,
        "status": "exploratory_unfrozen",
        "manifest_sha256": manifests,
        "findings": findings,
        "near_metric": "RapidFuzz Levenshtein.normalized_similarity",
        "normalization": "casefold, NFKD, remoção de acentos, tokens alfanuméricos separados por espaço",
        "near_threshold": NEAR_THRESHOLD,
        "human_review": "Revisar vizinhos e amostra abaixo do limiar, famílias, rótulos e exposição prévia.",
        "comparisons": dict(comparisons),
        "queries_by_split": dict(Counter(q.split for q in queries)),
        "expected_classes": dict(Counter(j.expected_class for j in judgments)),
        "pending_judgments": sum(
            j.adjudication == "pending_human_review" for j in judgments
        ),
    }
