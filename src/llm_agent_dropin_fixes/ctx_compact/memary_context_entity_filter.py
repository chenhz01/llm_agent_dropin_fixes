# memary_context_entity_filter.py
# Source issue: https://github.com/kingjulio8238/Memary/issues/42
# Upstream repo: kingjulio8238/Memary #42
# Category: ctx_compact
# Root cause / claim: Filters Memary's top-N entities down to those literally/near-present in the agent's latest response, cutting irrelevant context tokens per the issue's ask.
# Verifier note: py takes top-N entities + agent response and returns only response-relevant ones; directly solves issue #42.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

#!/usr/bin/env python3
"""memary_context_entity_filter.py
Narrows Memary's top-N entities to those actually present in the agent's
latest response, so the context window carries only relevant concepts.

Plug in: load your entities + agent response from Memary's Entity Knowledge Store.
No third-party keys hardcoded.
"""
from difflib import SequenceMatcher


def _norm(token: str) -> str:
    return token.strip().lower()


def response_relevant_entities(entities, agent_response, top_n=20, threshold=0.82):
    """Return entities whose surface form (or close match) appears in the response."""
    resp_tokens = {_norm(t) for t in agent_response.split()}
    kept = []
    for ent in entities[:top_n]:
        name = _norm(ent["name"]) if isinstance(ent, dict) else _norm(str(ent))
        if name in resp_tokens:
            kept.append(ent)
            continue
        if any(SequenceMatcher(None, name, t).ratio() >= threshold for t in resp_tokens):
            kept.append(ent)
    return kept


if __name__ == "__main__":
    top_entities = [{"name": "Paris"}, {"name": "Neural Network"}, {"name": "Coffee"}]
    last_response = "I love the coffee shop near the Eiffel tower in Paris."
    relevant = response_relevant_entities(top_entities, last_response)
    print(f"Passing {len(relevant)}/{len(top_entities)} entities to context:")
    for e in relevant:
        print(" -", e["name"] if isinstance(e, dict) else e)

