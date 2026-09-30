# cognee_contradiction_prefilter.py
# Source issue: https://github.com/topoteretes/cognee/issues/5221
# Upstream repo: topoteretes/cognee #5221
# Category: other
# Root cause / claim: 在 add_edges 前筛掉仅实体类型冲突（如 'qm is a person' vs 'qm is a feature'）的边，减少 ladybug UNREACHABLE_CODE 触发，保留事实性矛盾。
# Verifier note: py 针对 issue 里实体类型冲突占比高、触发断言的现象，做类型冲突预筛，可运行。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import re

# Pre-filter for cognee contradiction edges before add_edges.
# Plug in: run on detect_contradictions() output, before the graph adapter
# call at tasks/graph/detect_contradictions.py:235.

TYPE_VERB = re.compile(r"\b(is a|is an|are|type|instance of)\b", re.I)
RELN = re.compile(r"^(?P<subj>.+?)\s+(?:contradicts|conflicts with)\s+(?P<obj>.+?)\.?$", re.I)

def is_entity_type_conflict(text):
    """True when the conflict is only about an entity's *type*, not a fact
    (e.g. 'qm is a person' contradicts 'qm is a feature')."""
    if not TYPE_VERB.search(text):
        return False
    m = RELN.match(text)
    if not m:
        return False
    subj, obj = m.group("subj").strip(), m.group("obj").strip()
    return subj.split()[:1] == obj.split()[:1]   # same subject, different type noun

def filter_contradictions(edges, drop_type_conflicts=True):
    kept, dropped = [], []
    for e in edges:
        if drop_type_conflicts and is_entity_type_conflict(e.get("text", "")):
            dropped.append(e)   # these likely fired the ladybug assertion
        else:
            kept.append(e)      # factual contradictions -> keep
    return kept, dropped

# kept, dropped = filter_contradictions(contradiction_edges)
# graph_adapter.add_edges(kept)

