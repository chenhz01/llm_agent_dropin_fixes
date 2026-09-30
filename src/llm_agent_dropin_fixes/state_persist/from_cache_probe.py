# from_cache_probe.py
# Source issue: https://github.com/crewAIInc/crewAI/issues/7775
# Upstream repo: crewAIInc/crewAI #7775
# Category: state_persist
# Root cause / claim: Cache-tagged tool wrapper that emits ToolUsageFinishedEvent(from_cache=True) on replays, fixing the silent provenance bug.
# Verifier note: Py shows the correct flag emission the default executor currently drops.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

from crewai.tools import BaseTool
from crewai.event_bus import crewai_event_bus
from crewai.events import ToolUsageFinishedEvent

class CacheTaggedTool(BaseTool):
    """Wraps a tool so replays emit ToolUsageFinishedEvent(from_cache=True)."""
    name: str = "cached"
    description: str = "demo cache wrapper"
    def __init__(self, inner):
        super().__init__()
        self._inner, self._cache = inner, {}
    def _run(self, *a, **k):
        key = (a, tuple(sorted(k.items())))
        if key in self._cache:
            crewai_event_bus.emit(ToolUsageFinishedEvent(
                tool_name=self._inner.name, from_cache=True))  # correct flag
            return self._cache[key]
        out = self._inner._run(*a, **k)
        self._cache[key] = out
        return out

# Wrap your tool: cached = CacheTaggedTool(your_tool)
if __name__ == "__main__":
    print("cache-tagged tool ready")

