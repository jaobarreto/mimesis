"""Medição de fixtures de carga em processos Linux isolados."""

import argparse
import json
import platform
import resource
import sqlite3
from contextlib import closing
from time import perf_counter_ns, process_time_ns

from research_compiler.projection import create_projection, normalize
from research_experiment.engine import Experiment
from research_experiment.fixtures import records
from research_experiment.retrieval import exact

SIZES = (100, 1000, 10000, 50000, 100000)


def measure(size):
    if size not in SIZES:
        raise ValueError("Fixture de carga desconhecida")
    cpu = process_time_ns()
    start = perf_counter_ns()
    with Experiment() as core:
        core_init_ms = (perf_counter_ns() - start) / 1e6
        core_digest = core.info["logical_sha256"]
    start = perf_counter_ns()
    rows = [(f"load-{i}", (f"Carga {i}?",), (f"Resultado {i}.",)) for i in range(size)]
    knowledge = records(rows)
    del rows
    for record in knowledge.values():
        record["source_id"] = "synthetic-load-v1"
    with closing(sqlite3.connect(":memory:")) as db:
        db.execute("PRAGMA temp_store=MEMORY")
        info = {"fixture": "synthetic-load-v1"}
        before_build = perf_counter_ns()
        create_projection(db, knowledge, info)
        ready = perf_counter_ns()
        del knowledge
        t = perf_counter_ns()
        db.execute("INSERT INTO prompt_fts(prompt_fts) VALUES('rebuild')")
        db.commit()
        rebuild_ms = (perf_counter_ns() - t) / 1e6
        db.execute("PRAGMA query_only=ON")
        samples = []
        for i in range(25):
            key = normalize(f"Carga {(i * 7919) % size}?")
            t = perf_counter_ns()
            hits = exact(db, key, set())
            samples.append((perf_counter_ns() - t) / 1e6)
            if len(hits) != 1 or hits[0].key != key:
                raise RuntimeError("Recuperação de carga divergente")
        pages = db.execute("PRAGMA page_count").fetchone()[0]
        page_size = db.execute("PRAGMA page_size").fetchone()[0]
        if any(row[2] for row in db.execute("PRAGMA database_list")):
            raise RuntimeError("Projeção fora da memória")
    return {
        "records": size,
        "fixture": info["fixture"],
        "logical_sha256": info["logical_sha256"],
        "core_sha256": core_digest,
        "sqlite": sqlite3.sqlite_version,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "core_init_ms": core_init_ms,
        "load_ready_ms": (ready - start) / 1e6,
        "build_with_indexes_ms": (ready - before_build) / 1e6,
        "fts_rebuild_ms": rebuild_ms,
        "exact_lookup_ms": samples,
        "cpu_ms": (process_time_ns() - cpu) / 1e6,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "sqlite_logical_bytes": pages * page_size,
        "sqlite_disk_bytes": 0,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", required=True, type=int, choices=SIZES)
    print(json.dumps(measure(parser.parse_args().size)))
