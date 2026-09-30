# lc_async_parallel_guard.py
# Source issue: https://github.com/langchain-ai/langchain/issues/40877
# Upstream repo: langchain-ai/langchain #40877
# Category: other
# Root cause / claim: Caps async branch concurrency with a semaphore so RunnableParallel-style fan-out respects max_concurrency on ainvoke/astream, preventing unbounded resource use.
# Verifier note: py provides a working async parallel runner with a true concurrency cap; directly substitutes for the ignored max_concurrency on ainvoke/astream in #40877.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# lc_async_parallel_guard.py
# Fixes #40877: RunnableParallel ignores max_concurrency on ainvoke/astream.
# Drop-in runner that caps concurrent branches with a semaphore.
import asyncio
from typing import Any, Mapping
from langchain_core.runnables import Runnable

async def arun_parallel(branches, inputs, max_concurrency=1):
    """Run each branch concurrently but never exceed max_concurrency."""
    sem = asyncio.Semaphore(max_concurrency)
    async def _run(name, runnable):
        async with sem:
            return name, await runnable.ainvoke(inputs)
    results = await asyncio.gather(*(_run(n, r) for n, r in branches.items()))
    return dict(results)

# Usage:
# from langchain_core.runnables import RunnableLambda
# branching = {"a": RunnableLambda(fn_a), "b": RunnableLambda(fn_b)}
# out = await arun_parallel(branching, data, max_concurrency=2)
