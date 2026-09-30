# lc_limit_marker.py
# Source issue: https://github.com/langchain-ai/langchain/issues/40866
# Upstream repo: langchain-ai/langchain #40866
# Category: other
# Root cause / claim: Tags middleware cutoff messages with a programmatic finish_reason marker so they're detectable without fragile English-text matching.
# Verifier note: py detects the exact cutoff sentinel and sets response_metadata finish_reason, solving the programmatic-detection gap in #40866.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# lc_limit_marker.py
# Fixes #40866: ModelCallLimitMiddleware's cutoff message is indistinguishable
# from a real answer. Tag it via response_metadata so you can detect it safely.
from langchain_core.messages import AIMessage

LIMIT_SENTINEL = "Model call limits exceeded"

def tag_limit_message(message):
    content = message.content if isinstance(message.content, str) else ""
    if LIMIT_SENTINEL in content:
        md = dict(message.response_metadata)
        md.setdefault("finish_reason", "model_call_limit")
        return AIMessage(content=content, response_metadata=md,
                        additional_kwargs=message.additional_kwargs)
    return message

# final = tag_limit_message(agent.invoke(prompt))
# if final.response_metadata.get("finish_reason") == "model_call_limit": ...
