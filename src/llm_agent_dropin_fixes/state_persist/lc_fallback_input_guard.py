# lc_fallback_input_guard.py
# Source issue: https://github.com/langchain-ai/langchain/issues/40878
# Upstream repo: langchain-ai/langchain #40878
# Category: state_persist
# Root cause / claim: Prevents with_fallbacks from corrupting the caller's input state by deep-copying before the fallback path runs.
# Verifier note: py deep-copies inputs before with_fallbacks, guaranteeing the caller's dict is never mutated; directly addresses #40878.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# lc_fallback_input_guard.py
# Fixes #40878: with_fallbacks(exception_key=...) mutates the caller's input dict.
# Guard by deep-copying inputs so your original mapping stays clean.
import copy
from langchain_core.runnables import Runnable

def guarded_with_fallbacks(primary, fallbacks, inputs, exception_key="error",
                            is_async=False):
    """Deep-copy inputs, then run with_fallbacks so the original is untouched."""
    owned = copy.deepcopy(inputs)
    chain = primary.with_fallbacks(fallbacks, exception_key=exception_key)
    return chain.ainvoke(owned) if is_async else chain.invoke(owned)

# Usage:
# shared = {"a": 1}
# guarded_with_fallbacks(boom_chain, [fallback_chain], shared, exception_key="error")
# assert "error" not in shared   # caller's dict is unchanged
