# cognee_neo4j_metrics.py
# Source issue: https://github.com/topoteretes/cognee/issues/4832
# Upstream repo: topoteretes/cognee #4832
# Category: other
# Root cause / claim: 把全图 collect() 改写成 COUNT 轻量查询，并让 @deadlock_retry 跳过 MemoryPoolOutOfMemoryError，消除 OOM 重试风暴。
# Verifier note: py 直接对应 issue 的 collect 全图 + 重试放大两点，可运行。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Lightweight graph-summary for Neo4j + safe retry predicate.
# Plug in: replace get_model_independent_graph_data()'s collect() queries and
# guard @deadlock_retry so OOM is not retried 10x.

def graph_metrics_counts(tx):
    """Count queries instead of materializing the whole graph."""
    node_count = tx.run("MATCH (n:`__Node__`) RETURN count(n) AS c").single()["c"]
    edge_count = tx.run(
        "MATCH (n:`__Node__`)-[r]->(m:`__Node__`) RETURN count(r) AS c"
    ).single()["c"]
    return {"nodes": node_count, "edges": edge_count}

# Retry predicate: do NOT retry deterministic OOM.
OOM_MARKERS = ("MemoryPoolOutOfMemoryError", "OutOfMemoryError")

def should_retry(exc):
    msg = str(exc)
    if any(m in msg for m in OOM_MARKERS):
        return False   # give up fast; a retry just re-materializes + OOMs again
    return "Neo.TransientError" in msg  # only transient deadlocks

# metrics = graph_metrics_counts(tx)            # ~no GiB allocation
# if should_retry(e): retry() else: raise       # no 30 GiB storm

