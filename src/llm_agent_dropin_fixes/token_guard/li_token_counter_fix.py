# li_token_counter_fix.py
# Source issue: https://github.com/run-llama/llama_index/issues/23313
# Upstream repo: run-llama/llama_index #23313
# Category: token_guard
# Root cause / claim: 对 tool_calls 同时兼容 dict 形态并对 None 名称/参数做护栏，消除 TokenCounter 漏算与 TypeError。
# Verifier note: py 直接复现 dict tool_calls 计入 + None 跳过，确为 #23313 的计数/异常修复。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_token_counter_fix.py
# Fixes run-llama/llama_index#23313: dict tool_calls dropped + None TypeError.

def get_string_tokens(s) -> int:
    # Plug in your tokenizer here (tiktoken, llama tokenizer, ...)
    return len(s) if s is not None else 0

def count_message_tokens(messages) -> int:
    """messages: list of ChatMessage.to_dict() or raw OpenAI payloads."""
    total = 0
    for msg in messages:
        ak = msg.get("additional_kwargs", {}) or {}
        if "tool_calls" in ak:
            for tc in (ak.get("tool_calls") or []):
                fn = tc.get("function") if isinstance(tc, dict) else getattr(tc, "function", None)
                if fn is None:
                    continue
                name = fn.get("name") if isinstance(fn, dict) else getattr(fn, "name", None)
                args = fn.get("arguments") if isinstance(fn, dict) else getattr(fn, "arguments", None)
                total += get_string_tokens(name) + get_string_tokens(args) + 3
        total += get_string_tokens(msg.get("content") or "")
    return total

# --- self-test (no third-party deps) ---
msgs = [{"role": "assistant", "content": "",
         "additional_kwargs": {"tool_calls": [
             {"id": "c1", "type": "function", "function": {"name": "query_db", "arguments": '{"sql":"x"}'}},
             {"id": "c2", "type": "function", "function": {"name": None, "arguments": None}}]}}]
print(count_message_tokens(msgs))  # counts dict call + skips None safely
