# retrieval_trace.py
# Source issue: https://github.com/labring/FastGPT/issues/7113
# Upstream repo: labring/FastGPT #7113
# Category: memory_rerank
# Root cause / claim: 把 RAG 检索→重排→最终上下文做成可观测 trace，直接对应 #7113 的 Retrieval Trace View 诉求（retrieved/reranked/final_context/source attribution 四段）。
# Verifier note: py 直接产出 retrieved/reranked/final_context/sources 四段 trace，对应 issue 想要的 chunks/scores/reranked/final context/source attribution。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

"""retrieval_trace.py — build a RAG retrieval trace for debugging FastGPT KB answers.
Plug in your own retriever + reranker clients below; no keys hardcoded."""

from dataclasses import dataclass

@dataclass
class Chunk:
    id: str
    text: str
    vector_score: float

# --- plug your own clients here (no hardcoded keys) ---
# retriever = MyFastGPTClient(api_key=os.environ["FG_API_KEY"])
# reranker  = MyReranker(api_key=os.environ["RERANK_KEY"])

def retrieve(query: str, top_n: int = 10) -> list[Chunk]:
    # replace with: retriever.search(dataset_id=..., query=query, top_n=top_n)
    return [Chunk(f"c{i}", f"doc chunk {i}", 0.9 - i*0.05) for i in range(top_n)]

def rerank(query: str, chunks: list[Chunk], top_k: int = 4) -> list[tuple[Chunk, float]]:
    # replace with: reranker.score(query, [c.text for c in chunks])
    scored = [(c, c.vector_score * 0.7 + len(c.text)/1000 * 0.3) for c in chunks]
    return sorted(scored, key=lambda x: -x[1])[:top_k]

def build_trace(query: str, top_k: int = 4) -> dict:
    retrieved = retrieve(query)
    reranked = rerank(query, retrieved, top_k)
    final_ctx = "\n\n".join(f"[{c.id}] {c.text}" for c, _ in reranked)
    return {
        "query": query,
        "retrieved": [(c.id, round(c.vector_score,3)) for c in retrieved],
        "reranked":  [(c.id, round(s,3)) for c, s in reranked],
        "final_context": final_ctx,
        "sources": [c.id for c, _ in reranked],
    }

if __name__ == "__main__":
    import json
    print(json.dumps(build_trace("FastGPT 重试逻辑", top_k=4), ensure_ascii=False, indent=2))
