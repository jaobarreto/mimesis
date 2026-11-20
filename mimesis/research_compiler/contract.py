"""Contrato fechado do pacote local de Research."""

import hashlib
import json
import re
from datetime import datetime

ENGINE = "0.0.0"
SCHEMA = "0.1.0"
PROFILE = "research-dlg-v1"
OPERATIONS = {
    "access",
    "internal_copy",
    "extraction",
    "transformation",
    "local_query",
    "redistribution",
}
FILES = {"catalog.json", "records.jsonl"}


class InvalidPackage(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidPackage(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def parse(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"chave JSON repetida: {key}")
            result[key] = value
        return result

    def invalid(value):
        raise InvalidPackage(f"constante JSON inválida: {value}")

    value = json.loads(data.decode("utf-8"), object_pairs_hook=unique, parse_constant=invalid)
    canonical(value)  # Verifica que strings podem ser codificadas em UTF-8.
    return value


def fields(obj, names):
    require(isinstance(obj, dict) and set(obj) == set(names.split()), f"campos esperados: {names}")
    return obj


def string(value):
    require(isinstance(value, str) and value.strip() and "\x00" not in value, "texto inválido")
    return value


def positive(value):
    require(type(value) is int and 0 < value <= 2**63 - 1, "inteiro positivo inválido")
    return value


def sequence(value, *, empty=False):
    require(isinstance(value, list) and (value or empty), "lista inválida")
    return value


def strings(value, *, empty=False):
    items = [string(item) for item in sequence(value, empty=empty)]
    require(len(items) == len(set(items)), "elemento repetido na lista")
    return items


def date(value):
    require(
        re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?Z", string(value)
        ),
        "data UTC inválida",
    )
    datetime.fromisoformat(value)


def digest(value):
    require(re.fullmatch(r"[0-9a-f]{64}", string(value)), "SHA-256 inválido")
    return value


def version(value):
    require(
        re.fullmatch(r"(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*)){2}", string(value)), "versão inválida"
    )


def indexed(rows, names, key, *, empty=False):
    index = {}
    for row in sequence(rows, empty=empty):
        fields(row, names)
        identity = string(row[key])
        require(identity not in index, f"{key} duplicado: {identity}")
        index[identity] = row
    return index


def validate_manifest(m):
    fields(
        m,
        "knowledge_version schema_version engine_compatibility build_profile created_at artifacts records rights_summary",
    )
    version(m["knowledge_version"])
    require(
        m["schema_version"] == SCHEMA and m["build_profile"] == PROFILE,
        "esquema ou perfil incompatível",
    )
    versions = strings(m["engine_compatibility"])
    for item in versions:
        version(item)
    require(ENGINE in versions, "versão do compilador incompatível")
    date(m["created_at"])
    strings(m["rights_summary"])
    artifacts = indexed(m["artifacts"], "path byte_length sha256", "path")
    require(set(artifacts) == FILES, "artefatos do pacote incorretos")
    for artifact in artifacts.values():
        positive(artifact["byte_length"])
        digest(artifact["sha256"])
    records = indexed(m["records"], "record_id revision", "record_id")
    for record in records.values():
        positive(record["revision"])
    return artifacts, records


def validate_catalog(c):
    fields(c, "sources artifacts rights activities reviews")
    sources = indexed(
        c["sources"], "source_id source_type title creator source_locator checked_at", "source_id"
    )
    for source in sources.values():
        for value in source.values():
            string(value)
        date(source["checked_at"])
    rights = indexed(
        c["rights"],
        "rights_id evidence_locator scope jurisdiction decision reviewer_id reviewed_at obligations",
        "rights_id",
    )
    for right in rights.values():
        for key in ("evidence_locator", "jurisdiction", "reviewer_id"):
            string(right[key])
        require(right["decision"] == "approved", "parecer de direitos pendente ou recusado")
        require(set(strings(right["scope"])) == OPERATIONS, "escopo de direitos incompatível")
        strings(right["obligations"], empty=True)
        date(right["reviewed_at"])
    artifacts = indexed(
        c["artifacts"],
        "artifact_id source_id media_type byte_length sha256 storage_locator acquired_at rights_id",
        "artifact_id",
    )
    for artifact in artifacts.values():
        require(
            string(artifact["source_id"]) in sources and string(artifact["rights_id"]) in rights,
            "origem ou direitos do artefato ausentes",
        )
        string(artifact["media_type"])
        positive(artifact["byte_length"])
        digest(artifact["sha256"])
        string(artifact["storage_locator"])
        date(artifact["acquired_at"])
    activities = indexed(
        c["activities"],
        "activity_id input_ids output_ids operation tool_version config_digest agent_id occurred_at",
        "activity_id",
    )
    for activity in activities.values():
        strings(activity["input_ids"])
        strings(activity["output_ids"])
        for key in ("operation", "tool_version", "agent_id"):
            string(activity[key])
        digest(activity["config_digest"])
        date(activity["occurred_at"])
    reviews = indexed(c["reviews"], "record_id revision reviewer_ids decision", "record_id")
    for review in reviews.values():
        positive(review["revision"])
        require(
            review["decision"] == "approved" and len(strings(review["reviewer_ids"])) == 2,
            "dupla revisão ausente",
        )
    return artifacts, activities, reviews


def validate_records(rows, manifest, selected, catalog):
    artifacts, activities, reviews = validate_catalog(catalog)
    records = indexed(
        rows,
        "record_id revision domain schema_version language source_id rights_id provenance status payload",
        "record_id",
    )
    require(
        records.keys() == selected.keys() == reviews.keys(), "inventário de registros divergente"
    )
    used_rights = set()
    used_activities = set()
    used_artifacts = set()
    used_sources = set()
    for rid, record in records.items():
        revision = positive(record["revision"])
        require(
            revision == selected[rid]["revision"] == reviews[rid]["revision"], "revisão divergente"
        )
        require(record["status"] == "RELEASED", "registro sem liberação RELEASED")
        require(
            record["domain"] == "MKB-DLG"
            and record["language"] == "pt-BR"
            and record["schema_version"] == SCHEMA,
            "domínio, idioma ou esquema incompatível",
        )
        provenance = fields(record["provenance"], "artifact_id locator activity_ids")
        aid = string(provenance["artifact_id"])
        require(aid in artifacts, "artefato da linhagem ausente")
        artifact = artifacts[aid]
        string(provenance["locator"])
        require(
            record["source_id"] == artifact["source_id"]
            and record["rights_id"] == artifact["rights_id"],
            "origem ou direitos divergentes",
        )
        chain = strings(provenance["activity_ids"])
        previous = {aid}
        for event_id in chain:
            require(event_id in activities, "atividade ausente")
            event = activities[event_id]
            require(
                set(event["input_ids"]).issubset(previous), "entrada de atividade desconectada"
            )
            previous = set(event["output_ids"])
        require(f"{rid}@{revision}" in previous, "saída de atividade desconectada")
        used_rights.add(record["rights_id"])
        used_sources.add(record["source_id"])
        used_activities.update(chain)
        used_artifacts.add(aid)
        payload = fields(record["payload"], "prompts responses")
        for name, key in (("prompts", "prompt_id"), ("responses", "response_id")):
            children = indexed(payload[name], f"{key} text", key)
            for child in children.values():
                string(child["text"])
    require(
        used_rights
        == set(manifest["rights_summary"])
        == {row["rights_id"] for row in catalog["rights"]},
        "inventário de direitos divergente",
    )
    require(
        used_sources == {row["source_id"] for row in catalog["sources"]}
        and used_artifacts == set(artifacts)
        and used_activities == set(activities),
        "catálogo contém entidades fora da seleção",
    )
    return records
