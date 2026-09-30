# cognee_subgraph_normalize.py
# Source issue: https://github.com/topoteretes/cognee/issues/5031
# Upstream repo: topoteretes/cognee #5031
# Category: other
# Root cause / claim: 给出跨后端一致的 AND 分母（matched 而非 requested）、未知算子显式报错、无向边去重三处规范化实现。
# Verifier note: py 直接对应 issue 三个分歧点（AND 分母/算子校验/无向边双发），可运行。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Reference-correct behavior for get_nodeset_subgraph across backends.
# Plug in: use as the canonical semantics the adapters should agree on.

VALID_OPS = {"AND", "OR", "NOT"}

def normalize_operator(op):
    if op is None:
        return "AND"
    op = op.upper()
    if op not in VALID_OPS:
        raise ValueError(f"invalid node_name_filter_operator: {op!r}")  # not silent AND
    return op

def subgraph_match(names_requested, names_matched, op):
    """Consistent AND/OR semantics: count *matched* nodes, not requested."""
    op = normalize_operator(op)
    req, mat = set(names_requested), set(names_matched)
    if op == "AND":
        return req.issubset(mat)       # every requested name has a matched node
    if op == "OR":
        return bool(req & mat)
    return not (req & mat)             # NOT: none of the requested names matched

def dedup_undirected_edges(edges):
    """Ladybug returns each undirected edge twice; collapse to one."""
    seen, out = set(), []
    for a, b in edges:
        key = frozenset((a, b))
        if key in seen:
            continue
        seen.add(key); out.append((a, b))
    return out

# if subgraph_match(req, matched, op):  # AND uses matched denominator
#     render(dedup_undirected_edges(raw_edges))

