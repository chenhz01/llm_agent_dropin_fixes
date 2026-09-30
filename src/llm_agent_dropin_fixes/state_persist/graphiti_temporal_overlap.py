# graphiti_temporal_overlap.py
# Source issue: https://github.com/getzep/graphiti/issues/1865
# Upstream repo: getzep/graphiti #1865
# Category: state_persist
# Root cause / claim: Checks validity-interval overlap before reusing a historical edge, preserving disjoint occurrences.
# Verifier note: py returns False for disjoint intervals so a new edge is created.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_temporal_overlap.py
from datetime import datetime

def intervals_overlap(a_start, a_end, b_start, b_end):
    """True if two validity intervals intersect (None end = open)."""
    a_end = a_end or datetime.max.replace(tzinfo=b_start.tzinfo)
    b_end = b_end or datetime.max.replace(tzinfo=a_start.tzinfo)
    return a_start <= b_end and b_start <= a_end

def should_reuse_historical(new_edge, old_edge):
    """Reuse the historical edge only when the new occurrence overlaps it."""
    return intervals_overlap(
        new_edge.valid_at, new_edge.invalid_at,
        old_edge.valid_at, old_edge.invalid_at)

# In resolve_extracted_edge: skip historical-edge reuse when
# should_reuse_historical is False, so disjoint occurrences get their own edge.
