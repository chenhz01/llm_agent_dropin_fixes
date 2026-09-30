# li_memory_mac.py
# Source issue: https://github.com/run-llama/llama_index/issues/23246
# Upstream repo: run-llama/llama_index #23246
# Category: state_persist
# Root cause / claim: 对 memory 行计算 keyed MAC 并在 aget 校验，识别被篡改/重放的上下文行。
# Verifier note: self-test：篡改 data 后 verify_row 返回 False，对应 #23246。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_memory_mac.py
# Fixes run-llama/llama_index#23246: edited/replayed rows served as genuine context.
# Drop-in integrity check (inspired by the agmi reference store) over key+position+status+data.

import hashlib, hmac

SECRET = b"<plug in your per-user key>"   # derive from session key, never hardcode

def sign_row(key: str, position: int, status: str, data: str) -> str:
    msg = f"{key}|{position}|{status}|{data}".encode()
    return hmac.new(SECRET, msg, hashlib.sha256).hexdigest()

def verify_row(key: str, position: int, status: str, data: str, mac: str) -> bool:
    return hmac.compare_digest(sign_row(key, position, status, data), mac)

# --- self-test: an attacker rewrites `data`, MAC no longer matches ---
row = ("userA", 0, "active", "Paris is the capital of France")
mac = sign_row(*row)
tampered = ("userA", 0, "active", "Paris is the capital of Germany")
print(verify_row(*row, mac))                 # True
print(verify_row(*tampered, mac))            # False -> reject before aget()
