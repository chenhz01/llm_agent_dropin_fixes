# mem0_pinecone_l2_rescore.py
# Source issue: https://github.com/mem0ai/mem0/issues/7482
# Upstream repo: mem0ai/mem0 #7482
# Category: memory_rerank
# Root cause / claim: 突破组件：将 Pinecone 欧氏索引返回的 squared-distance 还原成单调递增相似度并重排，修复 Memory.search 在 L2 索引上丢最近记忆的问题。
# Verifier note: py 针对 issue 7482 的 euclidean 距离-as-score 错乱，样例里 near(0.0) 排到 far 之前。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Pinecone euclidean indexes return squared L2 distance as `score`, but mem0
# treats `score` as similarity. Convert it back so nearest wins.
# Plug in the raw hits from PineconeDB.search() (list of {id, score, ...}).
def l2_to_similarity(d: float) -> float:
    """Monotonic similarity: 0 distance -> 1.0, larger distance -> smaller."""
    return 1.0 / (1.0 + max(d, 0.0))

def rerank_euclidean(hits: list) -> list:
    for h in hits:
        h["score"] = l2_to_similarity(h.get("score", 0.0))
    return sorted(hits, key=lambda h: h["score"], reverse=True)

if __name__ == "__main__":
    raw = [{"id": "far", "score": 4.0}, {"id": "near", "score": 0.0}]
    for h in rerank_euclidean(raw):
        print(h["id"], round(h["score"], 3))
    # near (dist 0.0) -> 1.0 ; far -> 0.2 ; nearest listed first

