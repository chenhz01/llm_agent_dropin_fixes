# llm_failed_event_probe.py
# Source issue: https://github.com/crewAIInc/crewAI/issues/7783
# Upstream repo: crewAIInc/crewAI #7783
# Category: dedup
# Root cause / claim: Event-bus probe that counts LLMCallFailedEvent so the double-emission / scope-pop bug is reproducible in one run.
# Verifier note: Py reproduces the 2-vs-1 count the issue reports using a mock transport, no real API.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import httpx
from crewai import LLM
from crewai.event_bus import crewai_event_bus
from crewai.events import LLMCallFailedEvent

failed = []
@crewai_event_bus.on(LLMCallFailedEvent)
def _count(e):
    failed.append(e)

def _mock(req):
    return httpx.Response(400, json={"error": "boom"})

# Plug in your own model; client uses a mock transport (no real calls)
llm = LLM(model="gpt-4o", api_key="sk-test")
llm.client = httpx.Client(transport=httpx.MockTransport(_mock))

try:
    llm.call([{"role": "user", "content": "hi"}])
except Exception:
    pass

print("LLMCallFailedEvent count:", len(failed))  # repro shows 2, expect 1

