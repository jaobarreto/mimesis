import json
import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from mkb.adjudication import adjudicate, resolved
from mkb.pilot import connect, prepare


class AdjudicationTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.db = connect(Path(directory.name) / "test.db")
        self.addCleanup(self.db.close)
        prepare(self.db, Path(__file__).resolve().parents[1] / "pilot")
        self.row = self.db.execute(
            "select * from candidate where id='dlg-026'"
        ).fetchone()
        self.pair = "dlg-026-p2/dlg-026-r1"
        self.reason = {
            "summary": "Todos os pares funcionam no cenário.",
            "pairs": {
                self.pair: "A resposta concede licença também à segunda formulação."
            },
        }

    def ballots(self, disagrees=True, unanimous_reject=False):
        for reviewer in ("Ana", "Beto"):
            for i in (1, 2):
                for j in (1, 2):
                    reject = (
                        (i, j) == (2, 1)
                        and reviewer == "Beto"
                        and disagrees
                        or (i, j) == (1, 1)
                        and unanimous_reject
                    )
                    self.db.execute(
                        "insert into ballot values(?,?,?,?,?,?,?,?)",
                        (
                            "dlg-026",
                            1,
                            reviewer,
                            i,
                            j,
                            "reject" if reject else "accept",
                            "motivo de teste",
                            "2026-11-19",
                        ),
                    )
        self.db.commit()

    def decide(self, actor="Clara", verdict="accept", reason=None):
        return adjudicate(
            self.db,
            "dlg-026",
            1,
            actor,
            verdict,
            self.reason if reason is None else reason,
        )

    def test_evidence_replay_and_immutability(self):
        self.ballots()
        self.assertIsNone(resolved(self.db, self.row))
        result = ("accepted", ["Ana", "Beto"])
        self.assertEqual(self.decide(), result)
        self.assertEqual(self.decide(), result)
        self.assertEqual(resolved(self.db, self.row), result)
        saved = self.db.execute("select * from adjudication").fetchone()
        self.assertEqual(len(json.loads(saved["evidence"])["ballots"]), 8)
        self.assertEqual(json.loads(saved["reason"]), self.reason)
        with self.assertRaises(ValueError):
            self.decide(actor="Davi")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("delete from adjudication")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("update adjudication set actor='Outro'")
        self.db.execute("update ballot set reason='mudou' where reviewer='Ana'")
        with self.assertRaises(ValueError):
            resolved(self.db, self.row)

    def test_identity_pair_coverage_and_rejection(self):
        self.ballots()
        for actor, reason in [
            (" ANA ", self.reason),
            ("Clara", "Aprovo"),
            ("Clara", {"summary": "ok", "pairs": {"dlg-026-p1/dlg-026-r1": "ok"}}),
            ("Clara", {"summary": "ok", "pairs": {self.pair: " "}}),
        ]:
            with (
                self.subTest(actor=actor, reason=reason),
                self.assertRaises(ValueError),
            ):
                self.decide(actor=actor, reason=reason)
        self.assertEqual(
            self.decide(
                verdict="reject", reason="Separar as respostas em nova revisão."
            ),
            ("rejected", ["Ana", "Beto"]),
        )

    def test_unanimous_pair_rejection_blocks_whole_revision(self):
        self.ballots(unanimous_reject=True)
        with self.assertRaises(ValueError):
            self.decide()
        self.assertIsNone(resolved(self.db, self.row))
        self.assertEqual(self.decide(verdict="reject")[0], "rejected")

    def test_no_override_of_consensus_or_incomplete_matrix(self):
        self.ballots(disagrees=False)
        with self.assertRaises(ValueError):
            self.decide(verdict="reject", reason="Discordo.")
        self.db.execute(
            "delete from ballot where prompt=1 and response=1 and reviewer='Ana'"
        )
        self.db.commit()
        with self.assertRaisesRegex(ValueError, "incompleta"):
            self.decide()
