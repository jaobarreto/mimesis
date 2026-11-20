"""Constrói e verifica uma projeção SQLite fora do arquivo ativo."""

import hashlib
import os
import sqlite3
import sys
import unicodedata
from pathlib import Path
from tempfile import NamedTemporaryFile

from .contract import (
    ENGINE,
    PROFILE,
    SCHEMA,
    canonical,
    digest,
    parse,
    require,
    sha,
    validate_manifest,
    validate_records,
)

TOKENIZER = "unicode61 remove_diacritics 0"
CONFIG = {
    "normalization": "NFC-casefold-NFC-split-join",
    "tokenizer": TOKENIZER,
    "order": "binary-utf8",
    "unicode_version": unicodedata.unidata_version,
}


def normalize(text):
    folded = unicodedata.normalize("NFC", text).casefold()
    return " ".join(unicodedata.normalize("NFC", folded).split())


def read_inputs(package, expected_digest):
    def read(name):
        path = package / name
        require(path.is_file() and not path.is_symlink(), f"arquivo regular ausente: {name}")
        return path.read_bytes()

    manifest_bytes = read("manifest.json")
    require(sha(manifest_bytes) == digest(expected_digest), "SHA-256 do manifesto divergente")
    manifest = parse(manifest_bytes)
    artifacts, selected = validate_manifest(manifest)
    inputs = {}
    for name, artifact in artifacts.items():
        data = read(name)
        require(
            len(data) == artifact["byte_length"] and sha(data) == artifact["sha256"],
            f"tamanho ou SHA-256 divergente: {name}",
        )
        inputs[name] = data
    lines = inputs["records.jsonl"].split(b"\n")
    require(
        lines.pop() == b"" and b"\r" not in inputs["records.jsonl"],
        "JSONL requer UTF-8 e terminador LF",
    )
    records = validate_records(
        [parse(line) for line in lines], manifest, selected, parse(inputs["catalog.json"])
    )
    return manifest, records


def create_projection(db, records, info):
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript(f"""
        CREATE TABLE talkset(talkset_id TEXT PRIMARY KEY, revision INTEGER NOT NULL,
            language TEXT NOT NULL, source_id TEXT NOT NULL, rights_id TEXT NOT NULL,
            artifact_id TEXT NOT NULL, locator TEXT NOT NULL, activity_ids TEXT NOT NULL);
        CREATE TABLE prompt(prompt_id TEXT PRIMARY KEY, talkset_id TEXT NOT NULL REFERENCES talkset,
            text TEXT NOT NULL, normalized_text TEXT NOT NULL);
        CREATE INDEX prompt_key ON prompt(normalized_text);
        CREATE TABLE response(response_id TEXT PRIMARY KEY, talkset_id TEXT NOT NULL REFERENCES talkset,
            text TEXT NOT NULL);
        CREATE VIRTUAL TABLE prompt_fts USING fts5(normalized_text, content='prompt',
            content_rowid='rowid', tokenize='{TOKENIZER}');
        CREATE TABLE build_info(key TEXT PRIMARY KEY, value TEXT NOT NULL);
    """)
    for rid, record in sorted(records.items()):
        origin = record["provenance"]
        db.execute(
            "INSERT INTO talkset VALUES(?,?,?,?,?,?,?,?)",
            (
                rid,
                record["revision"],
                record["language"],
                record["source_id"],
                record["rights_id"],
                origin["artifact_id"],
                origin["locator"],
                canonical(origin["activity_ids"]).decode(),
            ),
        )
        for row in sorted(record["payload"]["prompts"], key=lambda p: p["prompt_id"]):
            db.execute(
                "INSERT INTO prompt VALUES(?,?,?,?)",
                (row["prompt_id"], rid, row["text"], normalize(row["text"])),
            )
        for row in sorted(record["payload"]["responses"], key=lambda r: r["response_id"]):
            db.execute(
                "INSERT INTO response VALUES(?,?,?)", (row["response_id"], rid, row["text"])
            )
    db.execute("INSERT INTO prompt_fts(prompt_fts) VALUES('rebuild')")
    db.execute("INSERT INTO prompt_fts(prompt_fts,rank) VALUES('integrity-check',1)")

    logical = hashlib.sha256()
    for table, count in (
        ("talkset", "talksets"),
        ("prompt", "prompts"),
        ("response", "responses"),
    ):
        size = 0
        for row in db.execute(f"SELECT * FROM {table} ORDER BY 1 COLLATE BINARY"):
            logical.update(canonical([table, *row]) + b"\n")
            size += 1
        info[count] = size
    info["logical_sha256"] = logical.hexdigest()
    db.executemany("INSERT INTO build_info VALUES(?,?)", sorted(info.items()))
    require(
        db.execute("PRAGMA integrity_check").fetchall() == [("ok",)], "falha de integridade SQLite"
    )
    require(not db.execute("PRAGMA foreign_key_check").fetchall(), "referência quebrada em SQLite")
    db.commit()


def compile_package(package, output, manifest_sha256):
    package = Path(package).resolve(strict=True)
    output = Path(output).absolute()
    require(
        output.suffix == ".sqlite"
        and not output.is_symlink()
        and not output.resolve().is_relative_to(package),
        "destino deve ser .sqlite fora do pacote",
    )
    for suffix in ("-wal", "-shm", "-journal"):
        require(not Path(str(output) + suffix).exists(), "destino SQLite possui transação lateral")
    manifest, records = read_inputs(package, manifest_sha256)
    info = {
        "engine_version": ENGINE,
        "schema_version": SCHEMA,
        "knowledge_version": manifest["knowledge_version"],
        "build_profile": PROFILE,
        "config_sha256": sha(canonical(CONFIG)),
        "manifest_sha256": manifest_sha256,
        "sqlite_version": sqlite3.sqlite_version,
        "unicode_version": unicodedata.unidata_version,
        "python_version": ".".join(map(str, sys.version_info[:3])),
    }
    with NamedTemporaryFile(
        dir=output.parent, prefix=".mimesis-", suffix=".sqlite", delete=False
    ) as temp:
        temp_path = Path(temp.name)
    try:
        db = sqlite3.connect(temp_path)
        try:
            create_projection(db, records, info)
        finally:
            db.close()
        with temp_path.open("rb") as verified:
            os.fsync(verified.fileno())
            info["sqlite_sha256"] = hashlib.file_digest(verified, "sha256").hexdigest()
        os.replace(temp_path, output)
    finally:
        temp_path.unlink(missing_ok=True)
    return info
