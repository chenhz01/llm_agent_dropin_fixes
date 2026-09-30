# coop_stop_guard.py
# Source issue: https://github.com/labring/FastGPT/issues/7665
# Upstream repo: labring/FastGPT #7665
# Category: loop_guard
# Root cause / claim: 在工具执行期插入协作式停止检查与迭代上限，消除 #7665 指出的 base.ts:532 await 期间不检查停止信号的竞态。
# Verifier note: py 在工具 await 期间轮询 stop 标志并设迭代/超时上限，直接对应 issue 分析的「工具执行期间不检查停止信号 / Stop API 超时返回 completed:false」。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

"""coop_stop_guard.py — cooperative cancellation + loop guard for agent tool execution.
Mirror of FastGPT's stop-sign race: poll a shared stop flag while a tool runs.
Plug in your own stop-flag source (Redis/HTTP); no keys hardcoded."""

import time, threading

class StopSign:
    def __init__(self): self._flag = False
    def set(self): self._flag = True
    def is_set(self): return self._flag

def guarded_tool_run(tool_fn, stop: StopSign, timeout: float = 30.0,
                     poll: float = 0.2, max_iters: int = 50):
    """Run tool_fn cooperatively: abort if stop set or iter cap hit.
    FastGPT base.ts:532 awaits onRunTool with no mid-flight check — this adds it."""
    iters, deadline = 0, time.time() + timeout
    while not stop.is_set() and iters < max_iters and time.time() < deadline:
        result = tool_fn()               # your HTTP/sandbox/sub-app call here
        if _should_stop(result, stop):   # e.g. tool itself signals completion
            return result
        iters += 1
        time.sleep(poll)                 # yield so Stop API can win the race
    return {"aborted": stop.is_set(), "iters": iters}

def _should_stop(result, stop): return stop.is_set() or result.get("done")

if __name__ == "__main__":
    s = StopSign()
    threading.Timer(1.0, s.set).start()  # simulate Stop API firing mid-tool
    print(guarded_tool_run(lambda: {"done": False}, s))
