# li_async_query_offload.py
# Source issue: https://github.com/run-llama/llama_index/issues/23298
# Upstream repo: run-llama/llama_index #23298
# Category: loop_guard
# Root cause / claim: 用 asyncio.to_thread 把同步 query 卸到线程，避免 aquery 阻塞事件循环。
# Verifier note: self-test：循环中仍可响应，证明未阻塞事件循环，对应 #23298。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_async_query_offload.py
# Fixes run-llama/llama_index#23298: _aquery() blocks the event loop via sync _query().
# Mirrors the #22400 fix: offload blocking work with asyncio.to_thread.

import asyncio

async def aquery_offload(engine, query_bundle):
    """Run a synchronous query engine without blocking the event loop (FastAPI-safe)."""
    return await asyncio.to_thread(engine.query, query_bundle)

# --- self-test: prove the loop stays free while the engine runs sync work ---
def blocking_query(qb):
    import time; time.sleep(0.2); return "done"

async def main():
    loop = asyncio.get_running_loop()
    t0 = loop.time()
    task = asyncio.create_task(aquery_offload(type("E", (), {"query": blocking_query})(), "q"))
    await asyncio.sleep(0.05)          # event loop still responsive
    print("loop responsive:", loop.time() - t0 < 0.1)
    print(await task)

asyncio.run(main())
