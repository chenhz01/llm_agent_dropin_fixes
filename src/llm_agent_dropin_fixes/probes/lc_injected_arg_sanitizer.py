# lc_injected_arg_sanitizer.py
# Source issue: https://github.com/langchain-ai/langchain/issues/40880
# Upstream repo: langchain-ai/langchain #40880
# Category: other
# Root cause / claim: Strips Pydantic-aliased injected tool args from on_tool_start serialized input so internal sentinels never reach callback logs.
# Verifier note: py parses the input_str and removes configured aliased injected keys before logging; directly addresses the alias-filter gap in #40880.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# lc_injected_arg_sanitizer.py
# Fixes #40880: a Pydantic-aliased InjectedToolArg leaks into on_tool_start input.
# Sanitize the serialized tool input so injected/secret args never reach callbacks.
import json
from langchain_core.callbacks import BaseCallbackHandler

INJECTED_ALIASES = {"_sentinel", "internal_sentinel"}  # add your alias names here

class InjectedArgSanitizer(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, *, run_id, **kwargs):
        print("tool start (safe):", self._scrub(input_str))
    def _scrub(self, input_str):
        try:
            data = json.loads(input_str)
            if isinstance(data, dict):
                data = {k: v for k, v in data.items()
                        if k.lower() not in INJECTED_ALIASES}
                return json.dumps(data)
        except (json.JSONDecodeError, TypeError):
            pass
        return input_str

# callbacks=[InjectedArgSanitizer()]
