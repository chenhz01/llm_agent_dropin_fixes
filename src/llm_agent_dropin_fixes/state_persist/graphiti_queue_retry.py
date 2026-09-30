# graphiti_queue_retry.py
# Source issue: https://github.com/getzep/graphiti/issues/1911
# Upstream repo: getzep/graphiti #1911
# Category: state_persist
# Root cause / claim: Retries transient ingest errors with backoff+jitter and re-queues episodes left with 0 edges.
# Verifier note: py recovers episodes that fail on transient LLM/timeout errors.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_queue_retry.py
import asyncio, random

async def with_retry(fn, *, attempts=4, base=1.0, max_wait=30.0):
    """Retry transient ingest errors with exponential backoff + jitter.

    Returns (result, None) on success, or (None, last_exc) after exhaustion.
    """
    for i in range(attempts):
        try:
            return await fn(), None
        except (ValueError, TimeoutError, RuntimeError) as e:  # transient
            if i == attempts - 1:
                return None, e
            await asyncio.sleep(min(max_wait, base * 2 ** i * (0.5 + random.random())))
    return None, RuntimeError("unreachable")

async def requeue_zero_edge(ep, store):
    """Re-queue episodes left with 0 edges after a successful (retry) pass."""
    if await store.edge_count(ep.uuid) == 0:   # plug your store
        await store.enqueue(ep)

# Covers the LLM-empty / validation / query-timeout shapes from issue 1911.
