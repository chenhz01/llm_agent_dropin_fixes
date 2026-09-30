# mem0_qdrant_split_ops.py
# Source issue: https://github.com/mem0ai/mem0/issues/7468
# Upstream repo: mem0ai/mem0 #7468
# Category: rag_grounding
# Root cause / claim: 突破组件：把合并在同一字段上的多个操作符拆成独立 AND 条件，修复 Qdrant 只应用首个操作符导致被排除记忆被返回的 bug。
# Verifier note: py 针对 issue 7468 的操作符合并问题，把 ne+nin 拆成两个独立条件供 Qdrant 正确处理。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# mem0 merges two operators on one field into one dict, so Qdrant keeps only
# the first. Keep them as separate AND conditions. Plug in your filters.
def split_field_ops(filters: dict) -> dict:
    out = {"AND": []}
    for cond in filters.get("AND", [filters]):
        for field, ops in cond.items():
            if isinstance(ops, dict):
                for op, val in ops.items():
                    out["AND"].append({field: {op: val}})
            else:
                out["AND"].append({field: ops})
    return out

if __name__ == "__main__":
    f = {"AND": [{"status": {"ne": "archived"}}, {"status": {"nin": ["deleted"]}}]}
    print(split_field_ops(f))
    # AND of two separate {status: {ne:...}} and {status: {nin:...}}

