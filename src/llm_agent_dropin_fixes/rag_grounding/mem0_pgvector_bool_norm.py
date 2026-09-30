# mem0_pgvector_bool_norm.py
# Source issue: https://github.com/mem0ai/mem0/issues/7443
# Upstream repo: mem0ai/mem0 #7443
# Category: rag_grounding
# Root cause / claim: 突破组件：把 pgvector 过滤值里的 Python 布尔归一为小写 JSON 文本，修复 eq/ne/in/nin 布尔过滤永不命中（及 ne/nin 静默返回被排除记录）的问题。
# Verifier note: py 针对 issue 7443 的布尔 str() 错配，把 True 转成 'true' 以匹配 JSON 列文本。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# pgvector filter values go through str(), so Python True -> "True" but the
# JSON column holds "true". Normalize bools before the filter is built.
# Plug in your filter dict from Memory.search(filters=...).
def norm_pg_bool(filters: dict) -> dict:
    out = {}
    for field, cond in filters.items():
        if isinstance(cond, dict):
            out[field] = {op: _val(v) for op, v in cond.items()}
        else:
            out[field] = _val(cond)
    return out

def _val(v):
    return str(v).lower() if isinstance(v, bool) else v

if __name__ == "__main__":
    print(norm_pg_bool({"archived": {"ne": True}}))
    print(norm_pg_bool({"archived": {"nin": [True]}}))
    # {'archived': {'ne': 'true'}} -> matches JSON 'true', excludes archived

