"""Adjudicação humana de matrizes completas com divergência."""

from .pilot import Candidate, digest, encode, normalize, now


def _schema(db):
    db.execute("""create table if not exists adjudication (
        id text not null, rev integer not null, actor text not null,
        verdict text not null check(verdict in ('accepted','rejected')),
        reason text not null, evidence text not null, evidence_sha256 text not null,
        at text not null, primary key(id,rev), foreign key(id,rev) references candidate(id,rev))""")
    for action in ("update", "delete"):
        db.execute(f"""create trigger if not exists adjudication_no_{action}
                    before {action} on adjudication begin
                    select raise(abort,'adjudicação imutável'); end""")


def _evidence(db, row):
    key = (row["id"], row["rev"])
    record = Candidate.model_validate_json(row["data"])
    ballots = [
        dict(b)
        for b in db.execute(
            "select * from ballot where id=? and rev=? order by reviewer,prompt,response",
            key,
        )
    ]
    reviewers = sorted({b["reviewer"] for b in ballots})
    if len(reviewers) != 2 or len({normalize(r) for r in reviewers}) != 2:
        raise ValueError("são necessários dois revisores distintos")
    pairs = {
        (i, j): []
        for i in range(1, len(record.prompts) + 1)
        for j in range(1, len(record.responses) + 1)
    }
    for ballot in ballots:
        idx = (ballot["prompt"], ballot["response"])
        if (
            idx not in pairs
            or ballot["verdict"] not in {"accept", "reject"}
            or not ballot["reason"].strip()
        ):
            raise ValueError("parecer inválido")
        pairs[idx].append(ballot["verdict"])
    disputed = set()
    unanimous_reject = False
    for (i, j), votes in pairs.items():
        if len(votes) != 2:
            raise ValueError("matriz de pareceres incompleta")
        if len(set(votes)) == 2:
            disputed.add(f"{record.id}-p{i}/{record.id}-r{j}")
        elif votes[0] == "reject":
            unanimous_reject = True
    if not disputed:
        raise ValueError("a revisão não tem divergências")
    evidence = encode({"candidate": dict(row), "ballots": ballots})
    return evidence, reviewers, disputed, unanimous_reject


def adjudicate(db, record_id, revision, actor, verdict, reason):
    decision = {
        "accept": "accepted",
        "accepted": "accepted",
        "reject": "rejected",
        "rejected": "rejected",
    }.get(verdict)
    if not decision or not isinstance(actor, str) or not actor.strip():
        raise ValueError("informe adjudicador e decisão válidos")
    if isinstance(reason, str):
        reason = {"summary": reason, "pairs": {}}
    if not isinstance(reason, dict) or set(reason) != {"summary", "pairs"}:
        raise ValueError("informe summary e pairs na justificativa")
    if not isinstance(reason["summary"], str) or not reason["summary"].strip():
        raise ValueError("informe o motivo da decisão")
    reasons = reason["pairs"]
    if not isinstance(reasons, dict) or any(
        not isinstance(v, str) or not v.strip() for v in reasons.values()
    ):
        raise ValueError("informe o motivo de cada par")
    key = (record_id, revision)
    with db:
        # Reserve the writer before reading the immutable revision and both ballots.
        if not db.in_transaction:
            db.execute("begin immediate")
        _schema(db)
        row = db.execute("select * from candidate where id=? and rev=?", key).fetchone()
        if row is None:
            raise ValueError("revisão inexistente")
        evidence, reviewers, disputed, unanimous_reject = _evidence(db, row)
        if normalize(actor) in {normalize(r) for r in reviewers}:
            raise ValueError("o adjudicador deve ser independente dos revisores")
        if set(reasons) - disputed:
            raise ValueError("justificativa aponta par sem divergência")
        if decision == "accepted" and (unanimous_reject or set(reasons) != disputed):
            raise ValueError(
                "aceite integral exige justificar cada divergência e respeitar rejeições unânimes"
            )
        values = (
            actor.strip(),
            decision,
            encode(reason).decode(),
            evidence.decode(),
            digest(evidence),
        )
        prior = db.execute(
            """select actor,verdict,reason,evidence,evidence_sha256
                           from adjudication where id=? and rev=?""",
            key,
        ).fetchone()
        if prior is None:
            db.execute(
                "insert into adjudication values (?,?,?,?,?,?,?,?)",
                (*key, *values, now()),
            )
        elif tuple(prior) != values:
            raise ValueError("adjudicação imutável já registrada para a revisão")
    return decision, reviewers


def resolved(db, row):
    if (
        db.execute(
            "select 1 from sqlite_master where type='table' and name='adjudication'"
        ).fetchone()
        is None
    ):
        return None
    result = db.execute(
        "select * from adjudication where id=? and rev=?", (row["id"], row["rev"])
    ).fetchone()
    if result is None:
        return None
    evidence, reviewers, _, _ = _evidence(db, row)
    if (
        evidence.decode() != result["evidence"]
        or digest(evidence) != result["evidence_sha256"]
    ):
        raise ValueError("evidência da adjudicação diverge da revisão e dos pareceres")
    return result["verdict"], reviewers
