# lc_tool_error_kwargs.py
# Source issue: https://github.com/langchain-ai/langchain/issues/40881
# Upstream repo: langchain-ai/langchain #40881
# Category: other
# Root cause / claim: Restores per-tool run context to on_tool_error by stashing on_tool_start kwargs per run_id and merging them back at error time.
# Verifier note: py captures kwargs at on_tool_start and re-injects them into on_tool_error, filling the exact gap in #40881.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# lc_tool_error_kwargs.py
# Fixes #40881: on_tool_error loses the **kwargs that on_tool_start/on_tool_end get.
# Recover them by stashing kwargs per run_id at start time.
from langchain_core.callbacks import BaseCallbackHandler

class KwargsAwareToolHandler(BaseCallbackHandler):
    def __init__(self):
        self._tool_kwargs = {}
    def on_tool_start(self, serialized, input_str, *, run_id, **kwargs):
        self._tool_kwargs[str(run_id)] = kwargs
    def on_tool_end(self, output, *, run_id, **kwargs):
        self._tool_kwargs.pop(str(run_id), None)
    def on_tool_error(self, error, *, run_id, **kwargs):
        merged = {**self._tool_kwargs.get(str(run_id), {}), **kwargs}
        print("tool error", type(error).__name__, "ctx=", merged)

# callbacks=[KwargsAwareToolHandler()]
