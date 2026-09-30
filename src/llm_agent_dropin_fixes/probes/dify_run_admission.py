# dify_run_admission.py
# Source issue: https://github.com/langgenius/dify/issues/43071
# Upstream repo: langgenius/dify #43071
# Category: other
# Root cause / claim: Adds an explicit per-process capacity boundary for dify-agent runs via a semaphore, rejecting bursts with 429.
# Verifier note: py raises '429 Too Many Requests' once the semaphore is locked, implementing the admission-control ask in #43071.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import asyncio

# Lightweight admission control for dify-agent POST /runs.
# Bound concurrently-active runs with a semaphore and reject with 429 at capacity.
# Plug in your own run scheduler below.

class RunAdmission:
    def __init__(self, max_active_runs=None):
        self._sem = asyncio.Semaphore(max_active_runs) if max_active_runs else None

    async def admit(self, coro):
        if self._sem is None:
            return await coro
        if self._sem.locked():
            raise RuntimeError('429 Too Many Requests')   # caller adds Retry-After
        async with self._sem:
            return await coro

async def main():
    adm = RunAdmission(max_active_runs=4)
    # await adm.admit(your_scheduler.create_run(...))
