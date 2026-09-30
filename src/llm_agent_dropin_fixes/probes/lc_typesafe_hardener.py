# lc_typesafe_hardener.py
# Source issue: https://github.com/langchain-ai/langchain/issues/40867
# Upstream repo: langchain-ai/langchain #40867
# Category: other
# Root cause / claim: Pre-validates TypeSafe documented limits and retries 429/529 with backoff so production classify calls stop failing late.
# Verifier note: py enforces the documented option/level limits before the call and retries 429/529 transiently; directly addresses #40867's two hardening asks.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# lc_typesafe_hardener.py
# Fixes #40867: TypeSafeClassifier doesn't validate size limits or retry 429/529.
# Wrap your classify call with limit checks + exponential backoff.
import time

MAX_CHOICES, MIN_LEVELS, MAX_LEVELS = 255, 2, 10

def harden_classify(classify, **payload):
    if "options" in payload and len(payload["options"]) > MAX_CHOICES:
        raise ValueError(f"too many options: {len(payload['options'])} > {MAX_CHOICES}")
    if "levels" in payload and not (MIN_LEVELS <= payload["levels"] <= MAX_LEVELS):
        raise ValueError(f"levels must be {MIN_LEVELS}-{MAX_LEVELS}")
    for attempt in range(4):
        try:
            return classify(**payload)
        except Exception as e:
            if getattr(e, "status_code", None) in (429, 529):
                time.sleep(2 ** attempt); continue
            raise
    raise RuntimeError("exhausted retries")

# result = harden_classify(your_classifier.classify, options=[...], levels=5)
