# graphiti_repetition_loop_guard.py
# Source issue: https://github.com/getzep/graphiti/issues/1922
# Upstream repo: getzep/graphiti #1922
# Category: loop_guard
# Root cause / claim: Detects extract_edges repetition loops and re-rolls at higher temperature instead of resending the identical request.
# Verifier note: py breaks the low-temp loop without raising the token cap.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_repetition_loop_guard.py
import re
from collections import Counter

def detect_repetition_loop(text, min_repeats=3):
    """True if the same sentence/fact repeats >= min_repeats (the 1922 loop)."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return False
    return Counter(lines).most_common(1)[0][1] >= min_repeats

async def generate_with_loop_guard(client, prompt, temps=(0.0, 0.3, 0.7)):
    """Re-roll at a higher temperature when a repetition loop is detected."""
    last = None
    for t in temps:
        resp = await client.generate(prompt, temperature=t)  # plug your client
        last = resp
        if not detect_repetition_loop(resp):
            return resp
    return last  # gave up; caller can chunk the episode instead

# Catches the low-temp sampling loop without raising the token cap.
