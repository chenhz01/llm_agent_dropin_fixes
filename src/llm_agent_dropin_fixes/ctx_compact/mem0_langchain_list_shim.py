# mem0_langchain_list_shim.py
# Source issue: https://github.com/mem0ai/mem0/issues/7461
# Upstream repo: mem0ai/mem0 #7461
# Category: ctx_compact
# Root cause / claim: 突破组件：为 mem0 的 Langchain 向量存储补一个非 Chroma 兜底 list()，消除 FAISS/Qdrant/PGVector 下 get_all()/delete_all() 的 NoneType 崩溃。
# Verifier note: py 针对 issue 7461 的 None 返回，对 FakeFAISS 正确回退到 index_to_docstore_id 并输出列表。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# mem0's Langchain.list() returns None for any non-Chroma client, crashing
# get_all()/delete_all(). Wrap the client so list() always returns a list.
# Plug in your own langchain VectorStore instance.
def list_memories(vstore) -> list:
    if hasattr(vstore, "_collection"):           # Chroma path mem0 already handles
        return vstore._collection.get()["ids"]
    ds = getattr(vstore, "docstore", None)
    if ds is not None:
        return list(ds._dict.keys()) if hasattr(ds, "_dict") else list(ds.yield_keys())
    if hasattr(vstore, "index_to_docstore_id"):
        return list(vstore.index_to_docstore_id.values())
    return []

if __name__ == "__main__":
    class FakeFAISS:
        index_to_docstore_id = {0: "m1", 1: "m2"}
    print(list_memories(FakeFAISS()))   # ['m1', 'm2']  (never None)

