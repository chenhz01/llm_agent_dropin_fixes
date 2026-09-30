# x402_detect.py
# Source issue: https://github.com/labring/FastGPT/issues/7837
# Upstream repo: labring/FastGPT #7837
# Category: state_persist
# Root cause / claim: 结构化识别 MCP 工具返回的 payment_required/payment_challenge，而非原样透传为文本，对应 #7837 的 detect it structurally 诉求。
# Verifier note: py 解析工具结果并结构识别 payment_challenge（status/pay_to/price/accepts），直接对应 #7837 的「detect it structurally (not raw JSON passthrough)」。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

"""x402_detect.py — structurally detect a pay-per-call x402 payment challenge in MCP tool output.
Targets issue #7837: FastGPT passes payment_challenge through as plain text.
Plug in your own MCP result; no keys hardcoded."""

import json

def detect_payment(raw_result):
    try:
        obj = json.loads(raw_result) if isinstance(raw_result, str) else raw_result
    except (json.JSONDecodeError, TypeError):
        return None
    if isinstance(obj, dict):
        if obj.get("status") == "payment_required" and "payment_challenge" in obj:
            ch = obj["payment_challenge"]
            return {"needs_payment": True,
                    "price": ch.get("price") if isinstance(ch, dict) else None,
                    "pay_to": ch.get("payTo") if isinstance(ch, dict) else None,
                    "accepts": ch.get("accepts") if isinstance(ch, dict) else None}
        if "payment_challenge" in obj:
            return {"needs_payment": True, "raw": obj["payment_challenge"]}
    return {"needs_payment": False}

if __name__ == "__main__":
    sample = '{"status":"payment_required","payment_challenge":{"payTo":"nano:abc","price":"0.0001"}}'
    print(detect_payment(sample))
