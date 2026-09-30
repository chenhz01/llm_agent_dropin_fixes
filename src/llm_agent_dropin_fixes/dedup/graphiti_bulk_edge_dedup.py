# graphiti_bulk_edge_dedup.py
# Source issue: https://github.com/getzep/graphiti/issues/1872
# Upstream repo: getzep/graphiti #1872
# Category: dedup
# Root cause / claim: Merges identical facts across a bulk batch into one edge with combined episode uuids.
# Verifier note: py yields one edge with episodes={ep1,ep2}.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_bulk_edge_dedup.py
def merge_bulk_resolutions(resolutions):
    """Collapse identical facts across a batch into one edge.

    resolutions: list of (edge, duplicates) where edge has .episodes (list).
    Returns list of surviving edges with combined episode uuids.
    """
    by_key = {}
    for edge, dups in resolutions:
        key = (edge.source_node_uuid, edge.target_node_uuid, _norm(edge.fact))
        if key not in by_key:
            by_key[key] = edge
        for d in dups:
            if d.uuid not in by_key[key].episodes:
                by_key[key].episodes.append(d.uuid)
    return list(by_key.values())

def _norm(s):
    return " ".join(s.lower().split())

# Replaces the fast-path `return resolved, [], []` so duplicates reach
# compress_uuid_map and one edge survives with episodes={ep1,ep2}.
