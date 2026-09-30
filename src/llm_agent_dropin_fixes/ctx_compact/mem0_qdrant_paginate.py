# mem0_qdrant_paginate.py
# Source issue: https://github.com/mem0ai/mem0/issues/7454
# Upstream repo: mem0ai/mem0 #7454
# Category: ctx_compact
# Root cause / claim: 突破组件：把 Qdrant 单页 list() 改成跟随 offset 的全量滚动，消除实体存储/批量清理在 1 万行处静默截断。
# Verifier note: py 针对 issue 7454 的 10k 截断，样例 14,883 行被完整遍历而非停在 10,000。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Qdrant.list() returns a single scroll page and stops at 10k rows, so
# entity-store scans miss everything after the first page. Paginate instead.
# Plug in your own Qdrant client + collection name.
def scroll_all(qclient, collection: str, batch: int = 10000):
    next_off = None
    seen = 0
    while True:
        pts, next_off = qclient.scroll(
            collection_name=collection, limit=batch, offset=next_off,
            with_payload=True, with_vectors=False,
        )
        if not pts:
            break
        seen += len(pts)
        yield from pts
        if next_off is None:
            break
    return seen

if __name__ == "__main__":
    class QC:
        def scroll(self, **k):
            off = k.get("offset") or 0
            if off >= 14883:
                return [], None
            nxt = off + 10000 if off + 10000 < 14883 else None
            return [{"id": i} for i in range(off, min(off + 10000, 14883))], nxt
    total = sum(1 for _ in scroll_all(QC(), "c"))
    print("rows seen:", total)   # 14883, not 10000

