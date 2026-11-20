import hashlib
import io
import json
import shutil
import tempfile
import unittest
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from mkb.importer import extract, import_file, strict_json_loads


def sha(data):
    return hashlib.sha256(data).hexdigest()


class IntakeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.input = self.root / "input.txt"
        self.input.write_bytes("ação\r\nfim".encode())
        (self.root / "evidence.txt").write_bytes(b"test evidence")
        self.path = self.root / "decision.json"
        self.store = self.root / "store"
        self.decision = {
            "source_id": "s1",
            "rights_id": "r1",
            "evidence_locator": "evidence.txt",
            "reviewer_id": "reviewer",
            "reviewed_at": "2026-11-19T00:00:00Z",
            "jurisdiction": "BR",
            "obligations": [],
            "artifact_sha256": sha(self.input.read_bytes()),
            "evidence_sha256": sha(b"test evidence"),
            "scope": {"copy_internal": "allowed", "extract": "allowed"},
        }
        self.save()

    def save(self):
        self.path.write_text(json.dumps(self.decision))

    def ingest(self):
        return import_file(self.input, self.path, self.store)

    def test_idempotent_concurrent_and_traceable(self):
        with ThreadPoolExecutor(2) as pool:
            first, second = pool.map(lambda _: self.ingest(), range(2))
        self.assertEqual(first, second)
        receipt = json.loads((first / "receipt.json").read_text())
        self.assertEqual(
            (self.store / receipt["storage_locator"]).read_bytes(),
            self.input.read_bytes(),
        )
        lines = (first / "units.jsonl").read_bytes()
        self.assertEqual(receipt["units_sha256"], sha(lines))
        self.assertEqual(
            json.loads(lines.splitlines()[0]), {"locator": "line:1", "text": "ação"}
        )
        self.decision["rights_id"] = "r2"
        self.save()
        self.assertNotEqual(self.ingest(), first)
        self.assertEqual(len(list((self.store / "objects").iterdir())), 1)
        (first / "units.jsonl").write_text("alterado")
        self.decision["rights_id"] = "r1"
        self.save()
        with self.assertRaises(ValueError):
            self.ingest()

    def test_requires_permissions_and_evidence_before_storage(self):
        self.decision["scope"]["extract"] = "unresolved"
        self.save()
        with self.assertRaises(ValueError):
            self.ingest()
        self.decision["scope"]["extract"] = "allowed"
        self.save()
        (self.root / "evidence.txt").write_text("alterado")
        with self.assertRaises(ValueError):
            self.ingest()
        (self.root / "evidence.txt").write_bytes(b"test evidence")
        self.input.write_text("outra edição")
        with self.assertRaises(ValueError):
            self.ingest()
        self.assertFalse(self.store.exists())

    def test_structured(self):
        self.assertEqual(
            list(extract(b'[{"a":null},"x"]', "json"))[1]["locator"], "json:/1"
        )
        self.assertEqual(
            list(extract(b'{"a":1}\n{"a":"y"}\n', "jsonl"))[1]["locator"], "line:2"
        )
        rows = list(extract(b'a,b\r\n"x\ny",\r\n', "csv"))
        self.assertEqual(
            rows, [{"locator": "csv:row:1", "value": {"a": "x\ny", "b": ""}}]
        )
        for value in ('{"a":{"b":0,"b":1}}', "NaN", "1e999"):
            with self.assertRaises(ValueError):
                strict_json_loads(value)
        with self.assertRaises(ValueError):
            list(extract(b"a,a\n1,2\n", "csv"))

    def test_markup(self):
        for fmt in ("xml", "tei"):
            units = list(
                extract(
                    b'<sp who="m" xml:lang="pt"><p xml:id="a">sim<b>!</b>fim</p></sp>',
                    fmt,
                )
            )
            self.assertEqual([x["text"] for x in units], ["sim", "!", "fim"])
            self.assertEqual(units[-1]["locator"], "xml:1/1/1/tail")
            self.assertEqual(units[0]["speaker"], "m")
            self.assertEqual(units[0]["ancestor_id"], "a")
            with self.assertRaises(ValueError):
                list(
                    extract(b'<!DOCTYPE data SYSTEM "file:///tmp/absent"><data/>', fmt)
                )
        units = list(
            extract(b'<nav>menu</nav><aside id="n">nota</aside><p>sim</p>', "html")
        )
        self.assertEqual([x["text"] for x in units], ["nota", "sim"])
        self.assertEqual(units[0]["role"], "note")
        self.assertEqual(units[0]["anchor"], "n")

    def test_epub_spine(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, "w") as z:
            z.writestr(
                "META-INF/container.xml",
                '<container><rootfile full-path="b/pack.opf"/></container>',
            )
            z.writestr(
                "b/pack.opf",
                "<package><manifest>"
                '<item id="a" href="a.html" media-type="text/html"/>'
                '<item id="b" href="b.html" media-type="text/html"/>'
                '</manifest><spine><itemref idref="b"/><itemref idref="a"/></spine></package>',
            )
            z.writestr("b/a.html", "<p>A</p>")
            z.writestr("b/b.html", "<p>B</p>")
        units = list(extract(data.getvalue(), "epub"))
        self.assertEqual([u["text"] for u in units], ["B", "A"])
        self.assertEqual(units[0]["member"], "b/b.html")

    @unittest.skipUnless(shutil.which("pdftotext"), "requer Poppler")
    def test_textual_pdf(self):
        stream = b"BT /F1 12 Tf 40 40 Td (texto) Tj ET"
        objects = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>",
            (
                b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Contents 4 0 R "
                b"/Resources << /Font << /F1 5 0 R >> >> >>"
            ),
            b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        ]
        data = bytearray(b"%PDF-1.4\n")
        offsets = []
        for i, obj in enumerate(objects, 1):
            offsets.append(len(data))
            data.extend(b"%d 0 obj\n" % i + obj + b"\nendobj\n")
        start = len(data)
        data.extend(b"xref\n0 6\n0000000000 65535 f \n")
        for offset in offsets:
            data.extend(b"%010d 00000 n \n" % offset)
        data.extend(
            b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % start
        )
        units = list(extract(bytes(data), "pdf"))
        self.assertEqual(
            (units[0]["locator"], units[0]["text"].strip()), ("page:1", "texto")
        )
