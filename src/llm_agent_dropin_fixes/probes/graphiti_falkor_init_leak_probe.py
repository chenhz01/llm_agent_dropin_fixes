# graphiti_falkor_init_leak_probe.py
# Source issue: https://github.com/getzep/graphiti/issues/1934
# Upstream repo: getzep/graphiti #1934
# Category: other
# Root cause / claim: Counts un-awaited build_indices_and_constraints tasks per group to expose the clone() task leak.
# Verifier note: py flags leak when pending init tasks exceed group count.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_falkor_init_leak_probe.py
import asyncio

def count_pending_init_tasks():
    """Report un-awaited build_indices_and_constraints() tasks (the 1934 leak)."""
    leaks = {}
    for t in asyncio.all_tasks():
        name = t.get_name() or ""
        if "build_indices_and_constraints" in name:
            grp = t.get_coro().__qualname__ if hasattr(t, "get_coro") else str(t)
            leaks.setdefault(grp, 0)
            leaks[grp] += 1
    return leaks

async def watch(interval=1.0, steps=10):
    for _ in range(steps):
        n = count_pending_init_tasks()
        if n:
            print("pending init tasks:", n)  # expect ~1, not 1 per clone
        await asyncio.sleep(interval)

# Name clone tasks so they are attributable:
# self._init_task = loop.create_task(self.build_indices_and_constraints(),
#                                    name=f"init:{database}")
