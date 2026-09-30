# graphiti_falkor6_index_probe.py
# Source issue: https://github.com/getzep/graphiti/issues/1947
# Upstream repo: getzep/graphiti #1947
# Category: other
# Root cause / claim: Probes which FalkorDB createNodeIndex syntax the running server accepts, directly targeting the 6.0 'expected at most 1' break.
# Verifier note: py detects the failing map+props form vs working DDL form on a FalkorDB instance.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_falkor6_index_probe.py
# Plug in YOUR falkordb graph handle below (no hardcoded credentials).
# from falkordb import FalkorDB
# graph = FalkorDB(host="localhost", port=6379).select_graph("graphiti")

def _run(graph, cypher):
    try:
        graph.query(cypher)
        return "ok"
    except Exception as e:  # noqa: BLE001
        return f"error: {type(e).__name__}: {e}"

def probe_fulltext_index_form(graph, label="Entity", prop="name"):
    """Report which createNodeIndex syntax the running FalkorDB accepts."""
    forms = {
        "map+props": f"CALL db.idx.fulltext.createNodeIndex({{label:'{label}', stopwords:[]}}, '{prop}')",
        "legacy_pos": f"CALL db.idx.fulltext.createNodeIndex('{label}', '{prop}')",
        "new_ddl": f"CREATE FULLTEXT INDEX FOR (n:{label}) ON (n.{prop})",
    }
    return {name: _run(graph, q) for name, q in forms.items()}

if __name__ == "__main__":
    # print(probe_fulltext_index_form(graph))
    pass
