# graphiti_dedup_tiebreak.py
# Source issue: https://github.com/getzep/graphiti/issues/1916
# Upstream repo: getzep/graphiti #1916
# Category: dedup
# Root cause / claim: Breaks fuzzy-dedup ties on candidate uuid (sorted) so resolution is deterministic across processes.
# Verifier note: py returns the same winning node regardless of PYTHONHASHSEED.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_dedup_tiebreak.py
def resolve_best_match(shingles, candidates):
    """Deterministic fuzzy match: break ties on candidate uuid, not set order.

    candidates: list of (uuid, candidate_shingles) for existing nodes.
    Returns the winning uuid (stable across processes).
    """
    best_uuid, best_score = None, -1.0
    for uuid, csh in sorted(candidates, key=lambda x: x[0]):  # sort by uuid
        score = _jaccard(shingles, csh)
        if score > best_score:          # strict > keeps first on equal score
            best_score, best_uuid = score, uuid
    return best_uuid

def _jaccard(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0

# Replace the `for candidate_id in candidate_ids:` loop in dedup_helpers.py.
