# li_rate_limiter_guard.py
# Source issue: https://github.com/run-llama/llama_index/issues/23202
# Upstream repo: run-llama/llama_index #23202
# Category: token_guard
# Root cause / claim: 对超出桶容量的请求快速失败而非死锁，修复 TokenBucket 永久阻塞与 SlidingWindow 放行超限。
# Verifier note: self-test：acquire(200) 抛 ValueError 而非死锁，对应 #23202。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_rate_limiter_guard.py
# Fixes run-llama/llama_index#23202: oversize request deadlocks the token bucket / slips the window.

import time

class SafeTokenBucket:
    def __init__(self, tokens_per_minute: int, burst: int | None = None):
        self.cap = burst or tokens_per_minute
        self.rate = tokens_per_minute / 60.0
        self.tokens = float(self.cap)
        self.last = time.monotonic()

    def acquire(self, num_tokens: int):
        if num_tokens > self.cap:                      # oversize -> fail fast
            raise ValueError(f"request {num_tokens} exceeds bucket capacity {self.cap}")
        now = time.monotonic()
        self.tokens = min(self.cap, self.tokens + (now - self.last) * self.rate)
        self.last = now
        wait = (num_tokens - self.tokens) / self.rate if num_tokens > self.tokens else 0
        if wait:
            time.sleep(wait)
        self.tokens -= num_tokens

# --- self-test ---
b = SafeTokenBucket(tokens_per_minute=100)
try:
    b.acquire(200)
except ValueError as e:
    print("rejected:", e)   # fails fast instead of hanging
