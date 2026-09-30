# cline_ctx_compactor.py
# Source issue: https://github.com/cline/cline/issues/14694
# Upstream repo: cline/cline #14694
# Category: ctx_compact
# Root cause / claim: Trims/summarizes oldest turns to a token budget so large-context sessions don't silently lose the Hub connection (#14694).
# Verifier note: py compacts a 20-message list to a 400-token budget and prints kept count; demonstrates the missing compaction path.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# cline_ctx_compactor.py
# For #14694: a minimal context compactor. When a large-context model starts
# failing (Hub closed code=1006), trim oldest turns to a token budget instead
# of running out of room.

def estimate_tokens(text):
    return max(1, len(text) // 4)   # crude 4 chars/token; swap for a real tokenizer

def compact(messages, budget, summarizer=None):
    kept, used = [], 0
    for m in reversed(messages):
        cost = estimate_tokens(m["content"])
        if used + cost <= budget:
            kept.insert(0, m); used += cost
        elif summarizer and len(kept) > 1:
            summary = summarizer(m["content"])
            kept.insert(0, {"role": m["role"], "content": f"[summary] {summary}"})
            used += estimate_tokens(summary); break
        else:
            break
    return kept, used

# --- plug your own client/summarizer here (no hardcoded keys) ---
def my_summarizer(text):
    return text[:120] + ("..." if len(text) > 120 else "")

msgs = [{"role": "user", "content": f"turn {i} "*50} for i in range(20)]
out, used = compact(msgs, budget=400, summarizer=my_summarizer)
print(f"kept {len(out)} messages, ~{used} tokens (budget 400)")

