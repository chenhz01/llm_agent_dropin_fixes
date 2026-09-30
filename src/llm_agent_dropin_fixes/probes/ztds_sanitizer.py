# ztds_sanitizer.py
# Source issue: https://github.com/crewAIInc/crewAI/issues/7789
# Upstream repo: crewAIInc/crewAI #7789
# Category: other
# Root cause / claim: Local in-memory PII sanitizer with deterministic surrogates + length-ordered restore, zero network egress (ZTDS spirit).
# Verifier note: Py masks email/secret and restores exact cleartext; matches the issue's restore() requirement.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import re

# Minimal local, in-memory PII sanitiser (no network egress).
PATTERNS = {
    "EMAIL_TOKEN": re.compile(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}"),
    "API_SECRET_TOKEN": re.compile(r"(?i)(api[_-]?key|token|secret)[=:\s\"']+[\w-]{8,}"),
}

class ZTDSSanitizer:
    def __init__(self):
        self._map, self._n = {}, 0
    def sanitize(self, text):
        for name, rx in PATTERNS.items():
            for m in rx.finditer(text):
                self._n += 1
                tok = f"[{name}_{self._n}]"
                self._map[tok] = m.group(0)
                text = text.replace(m.group(0), tok)
        return text
    def restore(self, text):
        for tok in sorted(self._map, key=len, reverse=True):
            text = text.replace(tok, self._map[tok])
        return text

if __name__ == "__main__":
    s = ZTDSSanitizer()
    red = s.sanitize("mail a@b.com key=SUPERSECRET123")
    print(red)
    print(s.restore(red))

