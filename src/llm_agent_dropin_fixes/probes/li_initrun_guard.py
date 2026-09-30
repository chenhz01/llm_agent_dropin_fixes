# li_initrun_guard.py
# Source issue: https://github.com/run-llama/llama_index/issues/23153
# Upstream repo: run-llama/llama_index #23153
# Category: other
# Root cause / claim: 在 user_hist 为空时安全回落到末条非 system 消息，消除 init_run 的 IndexError。
# Verifier note: self-test：无 user 消息时返回 '' 不抛 IndexError，对应 #23153。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_initrun_guard.py
# Fixes run-llama/llama_index#23153: IndexError when chat_history lacks a user message.

from llama_index.core.llms import ChatMessage, MessageRole, TextBlock

def resolve_user_msg_str(chat_history) -> str:
    """Safe replacement for the user_hist[-1] lookup: never index an empty list."""
    user_hist = [m for m in chat_history if m.role == MessageRole.USER]
    if user_hist:
        return "\n".join(b.text for b in user_hist[-1].blocks if isinstance(b, TextBlock))
    # fall back to the last non-system message instead of crashing
    last = next((m for m in reversed(chat_history)
                 if m.role != MessageRole.SYSTEM), None)
    return last.content if last else ""

# --- self-test ---
hist = [ChatMessage(role=MessageRole.ASSISTANT, content="Hello, how can I help?")]
print(repr(resolve_user_msg_str(hist)))   # '' no IndexError
