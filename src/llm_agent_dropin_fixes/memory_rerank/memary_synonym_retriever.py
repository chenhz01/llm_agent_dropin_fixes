# memary_synonym_retriever.py
# Source issue: https://github.com/kingjulio8238/Memary/issues/49
# Upstream repo: kingjulio8238/Memary #49
# Category: memory_rerank
# Root cause / claim: Implements the LLMSynonymRetriever concept from issue #49: expands queries into synonyms then de-dupes retrieval hits to surface more relevant graph nodes.
# Verifier note: py expands a query via LLM into synonyms and unions/de-dupes store hits; maps to issue #49's synonym retriever ask.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

#!/usr/bin/env python3
"""memary_synonym_retriever.py
Minimal LLM-backed synonym retriever for graph/vector queries (the
LLMSynonymRetriever idea in #49). Expands a query into synonyms, then unions
retrieval so the knowledge graph surfaces more relevant nodes.

Plug in: your LLM client + your graph/vector store below.
No third-party keys hardcoded.
"""
from typing import List


def expand_query(query: str, llm) -> List[str]:
    """Ask the LLM for synonymous phrasings of the query."""
    prompt = f"List 3 synonymous search phrasings for: {query}. One per line."
    text = llm.complete(prompt)  # plug your client (OpenAI/LlamaIndex/etc.)
    return [query] + [l.strip("- ").strip() for l in text.splitlines() if l.strip()]


def retrieve(query: str, llm, store, k: int = 5) -> List[str]:
    hits = []
    for q in expand_query(query, llm):
        hits.extend(store.search(q, k))   # plug your graph/vector store
    seen, out = set(), []
    for h in hits:
        if h.id not in seen:
            seen.add(h.id)
            out.append(h)
        if len(out) >= k:
            break
    return out


if __name__ == "__main__":
    class _LLM:
        def complete(self, p):
            return "related topic\n similar concept\n alternate phrasing"
    class _Store:
        def search(self, q, k):
            return [type("N", (), {"id": q})()]
    print([n.id for n in retrieve("memory graph", _LLM(), _Store())])

