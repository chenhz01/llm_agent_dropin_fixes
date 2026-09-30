# graphiti_episode_search_rerank.py
# Source issue: https://github.com/getzep/graphiti/issues/1888
# Upstream repo: getzep/graphiti #1888
# Category: memory_rerank
# Root cause / claim: Reranks the full 2*limit candidate set before truncating to limit, so the cross-encoder sees all candidates.
# Verifier note: py lets limit=1 still pick the second, more relevant episode.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_episode_search_rerank.py
def episode_search_rerank(candidates, ranked_scores, limit):
    """Rerank ALL 2*limit candidates, THEN truncate to limit.

    candidates: episodic nodes from the fulltext fetch (size 2*limit).
    ranked_scores: list[float] aligned 1:1 with candidates (from cross-encoder).
    """
    order = sorted(range(len(candidates)),
                   key=lambda i: ranked_scores[i], reverse=True)
    return [candidates[i] for i in order[:limit]]

# Fix for search.py: score the full 2*limit list, slice only at the very end.
