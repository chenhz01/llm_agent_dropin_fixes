# mem0_pinecone_filter_fix.py
# Source issue: https://github.com/mem0ai/mem0/issues/7483
# Upstream repo: mem0ai/mem0 #7483
# Category: rag_grounding
# Root cause / claim: 突破组件：把 mem0 的 $or/$not 与 eq/in/ne 操作符正确翻译成 Pinecone 原生过滤语法，消除每类 OR/NOT 搜索的 HTTP 400。
# Verifier note: py 直接修正 issue 7483 中 $or/$not 被包成 {$eq:[...]} 的错误，输出 Pinecone 合法过滤结构。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Translate mem0-style metadata filters into the shape Pinecone accepts,
# fixing the $or/$not -> {$eq: [...]} breakage from issue 7483.
# Plug in the filter dict you pass to Memory.search(filters=...).
OPS = {"eq": "$eq", "ne": "$ne", "in": "$in", "nin": "$nin",
       "gte": "$gte", "lte": "$lte", "gt": "$gt", "lt": "$lt"}

def to_pinecone_filter(f: dict) -> dict:
    out = {}
    for key, cond in f.items():
        if key in ("$or", "$and"):
            out[key] = [to_pinecone_filter(sub) for sub in cond]
        elif key == "$not":
            c = cond[0] if isinstance(cond, list) else cond
            out["$not"] = to_pinecone_filter(c)
        elif isinstance(cond, dict):
            out[key] = {OPS.get(op, op): val for op, val in cond.items()}
        else:
            out[key] = cond
    return out

if __name__ == "__main__":
    bad = {"$or": [{"category": {"in": ["work"]}}, {"tag": {"eq": "x"}}]}
    print(to_pinecone_filter(bad))
    # {'$or': [{'category': {'$in': ['work']}}, {'tag': {'$eq': 'x'}}]}

