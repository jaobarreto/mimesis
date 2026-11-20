"""Importação local. Execute python3 -m mkb.importer --help no diretório do projeto."""

import argparse
import csv
import hashlib
import io
import json
import math
import os
import posixpath
import re
import resource
import stat
import subprocess
import tempfile
import zipfile
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from xml.etree.ElementTree import TreeBuilder
from xml.parsers import expat

VERSION = "1.0.0"
MAX_BYTES = 16 * 1024 * 1024
MAX_UNITS = 100_000
FORMATS = ["txt", "json", "jsonl", "csv", "xml", "tei", "epub", "html", "pdf"]
MEDIA = dict(
    zip(
        FORMATS,
        (
            "text/plain",
            "application/json",
            "application/x-ndjson",
            "text/csv",
            "application/xml",
            "application/tei+xml",
            "application/epub+zip",
            "text/html",
            "application/pdf",
        ),
    )
)


def require(check, message):
    if not check:
        raise ValueError(message)


def strict_json_loads(text):
    def pairs(items):
        obj = {}
        for key, value in items:
            require(key not in obj, "chave JSON duplicada")
            obj[key] = value
        return obj

    def finite(value):
        number = float(value)
        require(math.isfinite(number), "número JSON fora dos limites")
        return number

    return json.loads(
        text, object_pairs_hook=pairs, parse_float=finite, parse_constant=finite
    )


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(obj):
    return (
        json.dumps(
            obj,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def read_local(path, limit):
    with open(
        path, "rb", opener=lambda p, flags: os.open(p, flags | os.O_NONBLOCK)
    ) as stream:
        info = os.fstat(stream.fileno())
        require(
            stat.S_ISREG(info.st_mode) and info.st_size <= limit,
            "arquivo inválido ou grande demais",
        )
        data = stream.read(limit + 1)
        require(len(data) <= limit, "arquivo grande demais")
        return data


def check_decision(path):
    decision = strict_json_loads(read_local(path, 128 * 1024).decode("utf-8"))
    require(isinstance(decision, dict), "parecer inválido")
    for key in (
        "source_id",
        "rights_id",
        "reviewer_id",
        "reviewed_at",
        "jurisdiction",
        "evidence_locator",
        "artifact_sha256",
        "evidence_sha256",
    ):
        require(
            isinstance(decision.get(key), str) and decision[key].strip(),
            f"campo ausente: {key}",
        )
    for key in ("artifact_sha256", "evidence_sha256"):
        require(re.fullmatch("[a-f0-9]{64}", decision[key]), f"hash inválido: {key}")
    stamp = decision["reviewed_at"]
    require(stamp.endswith("Z"), "reviewed_at exige UTC")
    datetime.fromisoformat(stamp)
    require(
        isinstance(decision.get("obligations"), list)
        and all(isinstance(x, str) for x in decision["obligations"]),
        "obrigações inválidas",
    )
    scope = decision.get("scope")
    require(
        isinstance(scope, dict)
        and all(scope.get(op) == "allowed" for op in ("copy_internal", "extract")),
        "cópia interna e extração exigem autorização",
    )
    evidence = Path(decision["evidence_locator"])
    require(
        not evidence.is_absolute() and ".." not in evidence.parts,
        "localizador de evidência inválido",
    )
    resolved = (path.parent / evidence).resolve(strict=True)
    require(
        resolved.is_relative_to(path.parent.resolve()),
        "evidência fora do diretório do parecer",
    )
    content = read_local(resolved, MAX_BYTES)
    require(
        content.strip() and digest(content) == decision["evidence_sha256"],
        "evidência divergente",
    )
    return decision


def safe_xml(data):
    builder = TreeBuilder()
    parser = expat.ParserCreate(namespace_separator="}")
    depth = count = 0

    def name(qname):
        return "{" + qname if "}" in qname else qname

    def start(tag, attrs):
        nonlocal depth, count
        depth += 1
        count += 1
        require(depth <= 96 and count <= MAX_UNITS, "XML excede os limites")
        builder.start(name(tag), {name(k): v for k, v in attrs.items()})

    def end(tag):
        nonlocal depth
        depth -= 1
        builder.end(name(tag))

    def reject(*args):
        raise ValueError("DTD e entidades externas são proibidos")

    parser.StartDoctypeDeclHandler = parser.ExternalEntityRefHandler = reject
    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.CharacterDataHandler = builder.data
    parser.Parse(data, True)
    return builder.close()


def xml_units(node, path="1", context=None):
    context = dict(context or {})
    tag = node.tag.split("}")[-1]
    for attr, key in (
        ("{http://www.w3.org/XML/1998/namespace}id", "ancestor_id"),
        ("{http://www.w3.org/XML/1998/namespace}lang", "language"),
        ("who", "speaker"),
    ):
        if attr in node.attrib:
            context[key] = node.attrib[attr]
    if tag in ("note", "speaker", "head", "div"):
        context["role"] = tag
    if node.text and node.text.strip():
        yield {
            "locator": f"xml:{path}/text",
            "text": node.text,
            "element": tag,
            **context,
        }
    for i, child in enumerate(node, 1):
        child_path = f"{path}/{i}"
        yield from xml_units(child, child_path, context)
        if child.tail and child.tail.strip():
            yield {
                "locator": f"xml:{child_path}/tail",
                "text": child.tail,
                "element": tag,
                **context,
            }


class HtmlUnits(HTMLParser):
    ignored = frozenset({"head", "nav", "footer", "script", "style", "template"})
    void = frozenset(
        [
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        ]
    )

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.units = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.void:
            require(len(self.stack) < 128, "HTML profundo demais")
            self.stack.append((tag, dict(attrs)))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not data.strip() or any(tag in self.ignored for tag, _ in self.stack):
            return
        line, column = self.getpos()
        unit = {"locator": f"html:{line}:{column}", "text": data}
        for tag, attrs in self.stack:
            if attrs.get("id"):
                unit["anchor"] = attrs["id"]
            if tag == "aside" or attrs.get("epub:type") in ("footnote", "endnote"):
                unit["role"] = "note"
        require(len(self.units) < MAX_UNITS, "HTML grande demais")
        self.units.append(unit)


def html_units(data):
    parser = HtmlUnits()
    parser.feed(data.decode("utf-8-sig"))
    parser.close()
    return parser.units


def epub_units(data):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = archive.infolist()
        names = {m.filename for m in members}
        require(
            len(members) <= 2048
            and len(names) == len(members)
            and sum(m.file_size for m in members) <= MAX_BYTES * 2,
            "EPUB excede limites ou repete membro",
        )
        for name in names:
            require(
                not name.startswith("/")
                and "\\" not in name
                and ".." not in PurePosixPath(name).parts,
                "caminho EPUB inválido",
            )
        container = safe_xml(archive.read("META-INF/container.xml"))
        packages = container.findall(".//{*}rootfile")
        require(len(packages) == 1, "edição EPUB ambígua")
        package = packages[0].attrib["full-path"]
        opf = safe_xml(archive.read(package))
        manifest = {}
        for item in opf.findall("./{*}manifest/{*}item"):
            key = item.attrib["id"]
            require(key not in manifest, "id EPUB duplicado")
            manifest[key] = item.attrib
        total = 0
        for i, item in enumerate(opf.findall("./{*}spine/{*}itemref"), 1):
            entry = manifest[item.attrib["idref"]]
            if (
                item.get("linear") == "no"
                or "nav" in entry.get("properties", "").split()
            ):
                continue
            require(
                entry["media-type"] in ("application/xhtml+xml", "text/html"),
                "spine fora do perfil textual",
            )
            url = urlsplit(entry["href"])
            relative = unquote(url.path)
            require(
                not (
                    url.scheme
                    or url.netloc
                    or url.query
                    or relative.startswith("/")
                    or "\\" in relative
                ),
                "href EPUB inválido",
            )
            name = posixpath.normpath(
                posixpath.join(posixpath.dirname(package), relative)
            )
            require(name in names, "membro do spine ausente")
            total += archive.getinfo(name).file_size
            require(total <= MAX_BYTES * 2, "spine grande demais")
            for unit in html_units(archive.read(name)):
                yield {
                    **unit,
                    "locator": f"epub:{i}:{name}#{unit['locator']}",
                    "member": name,
                }


def pdf_limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_BYTES, MAX_BYTES))
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2))
    resource.setrlimit(resource.RLIMIT_CPU, (15, 15))


def pdf_units(data):
    require(data.startswith(b"%PDF-"), "cabeçalho PDF inválido")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "pages.txt"
        proc = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", "-", str(path)],
            input=data,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20,
            check=False,
            preexec_fn=pdf_limits,
        )
        require(proc.returncode == 0, "falha na leitura do PDF")
        pages = read_local(path, MAX_BYTES).decode().split("\f")
        for n, page in enumerate(pages, 1):
            if page.strip():
                yield {"locator": f"page:{n}", "text": page}


def extract(data, fmt):
    if fmt in ("xml", "tei"):
        yield from xml_units(safe_xml(data))
    elif fmt == "epub":
        yield from epub_units(data)
    elif fmt == "html":
        yield from html_units(data)
    elif fmt == "pdf":
        yield from pdf_units(data)
    else:
        raw = data.decode("utf-8-sig")
        if fmt == "csv":
            reader = csv.reader(io.StringIO(raw, newline=""), strict=True)
            header = next(reader, [])
            require(
                header and all(header) and len(header) == len(set(header)),
                "cabeçalho CSV inválido",
            )
            for i, row in enumerate(reader, 1):
                require(len(row) == len(header), "largura CSV inválida")
                yield {"locator": f"csv:row:{i}", "value": dict(zip(header, row))}
        elif fmt == "json":
            value = strict_json_loads(raw)
            if isinstance(value, list):
                for i, item in enumerate(value):
                    yield {"locator": f"json:/{i}", "value": item}
            else:
                yield {"locator": "json:", "value": value}
        else:
            for i, line in enumerate(io.StringIO(raw, newline=""), 1):
                if fmt == "jsonl":
                    require(line.strip(), "linha JSONL vazia")
                    value = strict_json_loads(line)
                    require(isinstance(value, dict), "JSONL exige um objeto por linha")
                    yield {"locator": f"line:{i}", "value": value}
                else:
                    yield {"locator": f"line:{i}", "text": line.rstrip("\r\n")}


def immutable_file(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent) as temp:
        temp.write(data)
        temp.flush()
        try:
            os.link(temp.name, path)
        except FileExistsError:
            require(read_local(path, len(data)) == data, "objeto armazenado divergente")


def import_file(input_path, decision_path, store, fmt=None):
    """Guarda uma única cópia dos bytes. Cada decisão e configuração tem recibo próprio."""
    input_path, decision_path, store = map(Path, (input_path, decision_path, store))
    fmt = fmt or input_path.suffix.lower().lstrip(".")
    require(fmt in FORMATS, "formato desconhecido")
    decision = check_decision(decision_path)
    data = read_local(input_path, MAX_BYTES)
    sha = digest(data)
    require(sha == decision["artifact_sha256"], "hash do original diverge do parecer")
    config = {"format": fmt, "importer": VERSION}
    if fmt in ("txt", "json", "jsonl", "csv", "html"):
        config["encoding"] = (
            "utf-8-sig" if data.startswith(b"\xef\xbb\xbf") else "utf-8"
        )
    if fmt == "csv":
        config.update(
            delimiter=",", quotechar='"', null_convention="all_fields_are_strings"
        )
    if fmt == "txt":
        config["line_endings"] = sorted(
            {match[0].decode("ascii") for match in re.finditer(b"\r\n|\r|\n", data)}
        )
    if fmt == "pdf":
        config["pdftotext"] = (
            subprocess.check_output(
                ["pdftotext", "-v"], stderr=subprocess.STDOUT, timeout=5
            )
            .decode()
            .splitlines()[0]
        )
    key = digest(encoded([sha, decision, config]))
    raw = Path("objects") / sha
    store.mkdir(parents=True, exist_ok=True)
    bundles = store / "intakes"
    bundles.mkdir(exist_ok=True)
    target = bundles / key
    with tempfile.TemporaryDirectory(dir=bundles) as temp:
        stage = Path(temp) / "bundle"
        stage.mkdir()
        count = size = 0
        units_hash = hashlib.sha256()
        with (stage / "units.jsonl").open("wb") as stream:
            for count, unit in enumerate(extract(data, fmt), 1):
                line = encoded(unit)
                size += len(line)
                require(
                    count <= MAX_UNITS and size <= MAX_BYTES * 4, "saída excede limites"
                )
                stream.write(line)
                units_hash.update(line)
        require(count, "sem unidades extraíveis")
        receipt = {
            "intake_id": key,
            "artifact_id": "sha256:" + sha,
            "sha256": sha,
            "source_id": decision["source_id"],
            "rights_id": decision["rights_id"],
            "storage_locator": raw.as_posix(),
            "media_type": MEDIA[fmt],
            "byte_length": len(data),
            "config": config,
            "status": "PROCESSED",
            "decision": decision,
            "unit_count": count,
            "units_sha256": units_hash.hexdigest(),
        }
        immutable_file(store / raw, data)
        now = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        (stage / "receipt.json").write_bytes(encoded({**receipt, "acquired_at": now}))
        try:
            stage.rename(target)
        except OSError:
            if not target.is_dir():
                raise
            existing = strict_json_loads(
                read_local(target / "receipt.json", 256 * 1024).decode()
            )
            existing.pop("acquired_at")
            require(
                existing == receipt
                and digest(read_local(target / "units.jsonl", size))
                == receipt["units_sha256"],
                "recibo existente divergente",
            )
    return target


def main():
    parser = argparse.ArgumentParser(
        description="Importa arquivo local segundo parecer com evidência e hash."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--decision", required=True, type=Path)
    parser.add_argument("--store", required=True, type=Path)
    parser.add_argument("--format", choices=FORMATS)
    args = parser.parse_args()
    try:
        print(import_file(args.input, args.decision, args.store, args.format))
    except (
        ValueError,
        TypeError,
        OSError,
        KeyError,
        RuntimeError,
        expat.ExpatError,
        zipfile.BadZipFile,
        csv.Error,
        subprocess.SubprocessError,
    ) as error:
        parser.exit(1, f"Importação interrompida: {error}\n")


if __name__ == "__main__":
    main()
