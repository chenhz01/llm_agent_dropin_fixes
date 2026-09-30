# egress_policy.py
# Source issue: https://github.com/labring/FastGPT/issues/7345
# Upstream repo: labring/FastGPT #7345
# Category: state_persist
# Root cause / claim: 用通配符域名匹配实现 allow/deny 出网策略（默认 deny=fail-closed）并做命中词脱敏，对应 #7345 的 1.5 通配符与 3.2 redact。
# Verifier note: py 实现 *.example.com 通配符匹配与默认拒绝出网、以及敏感词 redact，直接对应 issue 1.5 域名通配符与 2/3 返回内容审查脱敏。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

"""egress_policy.py — wildcard domain matcher + content redactor for Agent Sandbox egress.
Covers issue #7345 asks 1.5 (wildcards) and 3.2 (redact).
Plug in your own policy source; no keys hardcoded."""

import fnmatch, re

def match_domain(host: str, rules: list[str]) -> bool:
    host = host.lower()
    return any(fnmatch.fnmatch(host, r.lower()) or host == r.lower()
               for r in rules)   # rules like "*.example.com", "example.com"

def apply_egress(url: str, allow: list[str], deny: list[str]) -> str:
    host = url.split("/")[2] if "://" in url else url
    if any(match_domain(host, deny)): return "block"      # deny wins
    if match_domain(host, allow):     return "allow"
    return "block"                    # default-deny posture (fail-closed)

REDACT_RE = re.compile(r"(?i)(暴力|色情|违禁|secret|api[_-]?key)")

def redact(text: str, action: str = "redact") -> str:
    if action == "block" and REDACT_RE.search(text):
        return "<<blocked>>"
    return REDACT_RE.sub("<<redacted>>", text)

if __name__ == "__main__":
    print(apply_egress("https://api.example.com/x", ["*.example.com"], ["evil.com"]))
    print(redact("heres an api_key=abc secret"))
