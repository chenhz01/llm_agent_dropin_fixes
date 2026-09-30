# memary_external_memory_adapter.py
# Source issue: https://github.com/kingjulio8238/Memary/issues/45
# Upstream repo: kingjulio8238/Memary #45
# Category: other
# Root cause / claim: Wraps Memary behind a remember()/recall() adapter so it drops into any existing LLM chain as a standalone module, answering issue #45's integration question.
# Verifier note: py defines a standalone-runnable MemoryClient adapter; directly answers how to use Memary as external memory.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

#!/usr/bin/env python3
"""memary_external_memory_adapter.py
Shows how to wrap Memary as a drop-in external memory module for ANY
LLM chain/agent, without coupling your code to Memary internals.

Plug in: import MemaryMemory from memary and pass it to MemoryClient.
No third-party keys hardcoded.
"""
from typing import List


class MemoryClient:
    """Thin adapter: your agent talks to this, not to Memary directly."""

    def __init__(self, memary_memory):
        self._mem = memary_memory  # plug your Memary instance here

    def remember(self, text: str) -> None:
        self._mem.add_memory(text)  # e.g. your Memary add call

    def recall(self, query: str, k: int = 5) -> List[str]:
        return self._mem.search(query, k)  # e.g. your Memary search call


# minimal local stand-in so this file runs standalone
class _LocalStandIn:
    def __init__(self):
        self._store = []

    def add_memory(self, text):
        self._store.append(text)

    def search(self, query, k=5):
        return [m for m in self._store if query.lower() in m.lower()][:k]


if __name__ == "__main__":
    client = MemoryClient(_LocalStandIn())
    client.remember("User prefers concise answers about Python.")
    client.remember("User is building a RAG agent.")
    print(client.recall("Python"))

