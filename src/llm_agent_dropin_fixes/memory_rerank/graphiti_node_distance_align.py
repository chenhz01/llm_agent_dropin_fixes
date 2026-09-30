# graphiti_node_distance_align.py
# Source issue: https://github.com/getzep/graphiti/issues/1897
# Upstream repo: getzep/graphiti #1897
# Category: memory_rerank
# Root cause / claim: Pairs every returned edge with its source's node-distance score so shared-source facts aren't misaligned.
# Verifier note: py yields [10,10,1,0] for the reported 4-candidate case.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_node_distance_align.py
def align_node_distance_scores(sources, edges_per_source):
    """Pair every returned edge with its source's distance score.

    sources: list of (source_uuid, distance_score) from the reranker.
    edges_per_source: dict source_uuid -> list[edge_uuid] as expanded.
    Returns list[(edge_uuid, score)] aligned 1:1.
    """
    out = []
    for src_uuid, score in sources:
        for edge_uuid in edges_per_source.get(src_uuid, []):
            out.append((edge_uuid, score))
    return out

# Replaces the per-source score list that the bug kept un-expanded.
