# dify_hybrid_diagnostic.py
# Source issue: https://github.com/langgenius/dify/issues/42996
# Upstream repo: langgenius/dify #42996
# Category: memory_rerank
# Root cause / claim: Detects the vectorizer:none misconfiguration and embeds the query client-side so hybrid retrieval returns chunks even before the rebuild.
# Verifier note: py flags vectorizer:'none' and provides a client-side embed path; addresses the 0-chunk hybrid failure in #42996.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Diagnostic + query-side fallback for hybrid retrieval returning 0 chunks when
# the vector store was created with vectorizer:'none' (Weaviate + Ollama bge-m3).
# Plug in your own Weaviate client and embedding client below.

def check_vectorizer(collection_config):
    vec = (collection_config or {}).get('vectorizer', {})
    if 'none' in vec:   # query text won't be embedded server-side -> 0 hybrid hits
        return 'MISMATCH: add a vectorizer or embed the query client-side'
    return 'ok'

def hybrid_query(query, embed_fn, search_fn):
    vec = embed_fn(query)                 # plug: ollama bge-m3 / your provider
    return search_fn(query=query, vector=vec)   # plug: weaviate hybrid(alpha=0.5)

if __name__ == '__main__':
    # print(check_vectorizer(your_collection_config))
    # results = hybrid_query('2003年成立', embed_fn=your_embed, search_fn=your_search)
    pass
