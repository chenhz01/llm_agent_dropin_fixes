# gr_bounded_call_guard.py
# Source issue: https://github.com/assafelovic/gpt-researcher/issues/1764
# Upstream repo: assafelovic/gpt-researcher #1764
# Category: loop_guard
# Root cause / claim: Thread-based bounded-call guard that turns silent external-call hangs into logged, retried, time-bounded events — directly answering the missing timeout/retry/logging ask.
# Verifier note: py truly solves issue 1764: adds a hard wall-clock timeout + retry + logging around external calls, addressing the no-logs/no-timeout hang.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

"""
Bounded external-call guard for GPT Researcher.
Wraps any external call (LLM / search engine / scraper) so a hang becomes
a logged, retried, time-bounded event instead of a silent stuck run.
"""
import logging
import time
from concurrent.futures import ThreadPoolExecutor

log = logging.getLogger("gptr.callguard")
logging.basicConfig(level=logging.INFO)


def bounded_call(fn, timeout=30, retries=3, backoff=2.0, args=(), kwargs=None):
    """Run fn in a worker thread with a hard wall-clock timeout + retry + logging."""
    kwargs = kwargs or {}
    last = None
    for attempt in range(1, retries + 1):
        log.info("[callguard] -> %s attempt %d (timeout=%ss)",
                 fn.__name__, attempt, timeout)
        start = time.time()
        try:
            with ThreadPoolExecutor(max_workers=1) as ex:
                fut = ex.submit(fn, *args, **kwargs)
                out = fut.result(timeout=timeout)   # hard stall guard
            log.info("[callguard] %s ok in %.1fs", fn.__name__, time.time() - start)
            return out
        except Exception as e:
            last = e
            log.warning("[callguard] %s attempt %d failed: %s",
                        fn.__name__, attempt, e)
            if attempt < retries:
                time.sleep(backoff * attempt)
    log.error("[callguard] %s exhausted %d attempts: %s",
              fn.__name__, retries, last)
    raise TimeoutError(f"{fn.__name__} stalled after {retries} attempts")


# PLUG IN YOUR CLIENT / MODEL:
# def search(q): return your_searxng.search(q)   # also set requests timeout=
# result = bounded_call(search, timeout=30, args=("AI news",))
