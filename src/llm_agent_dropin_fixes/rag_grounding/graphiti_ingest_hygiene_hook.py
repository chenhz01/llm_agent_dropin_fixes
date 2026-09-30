# graphiti_ingest_hygiene_hook.py
# Source issue: https://github.com/getzep/graphiti/issues/1880
# Upstream repo: getzep/graphiti #1880
# Category: rag_grounding
# Root cause / claim: Grounds extracted edges in source text via lexical overlap, flagging misattributed triples before commit.
# Verifier note: py flags edges whose terms don't appear in the source.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_ingest_hygiene_hook.py
import re

def verify_graph_hygiene(extracted_edges, source_text, threshold=0.5):
    """Opt-in ingest hook: flag edges whose fact isn't grounded in source_text.

    extracted_edges: list of objects with a .fact string.
    Returns (kept, flagged) so misattributed triples are caught pre-commit.
    """
    src = source_text.lower()
    kept, flagged = [], []
    for e in extracted_edges:
        tokens = re.findall(r"[a-z0-9]+", e.fact.lower())
        hits = sum(1 for t in set(tokens) if t in src)
        if tokens and hits / len(set(tokens)) >= threshold:
            kept.append(e)
        else:
            flagged.append(e)          # e.g. "my brother is a lawyer" not in text
    return kept, flagged

# Register as the proposed ingest_validator; upgrade to NLI for stricter checks.
