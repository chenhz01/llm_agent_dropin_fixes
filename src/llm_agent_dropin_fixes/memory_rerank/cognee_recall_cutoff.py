# cognee_recall_cutoff.py
# Source issue: https://github.com/topoteretes/cognee/issues/5222
# Upstream repo: topoteretes/cognee #5222
# Category: memory_rerank
# Root cause / claim: 对 recall 结果做融合分阈值截断 + 标识符型词法 boost，让噪声 prompt 返回空、commit SHA/工单号精确命中回到前列。
# Verifier note: py 实现 min_score 截断（噪声返回空）与标识符 RRF 词法 boost（issue 所述两类 miss），对得上该 issue。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import re

# Post-retrieval filter for cognee recall results.
# Plug in: pass your recall() output as list of dicts with 'text' and 'score'.
# 'lexical_score' is optional (expose it from hybrid fusion if available).

SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
TICKET_RE = re.compile(r"\b(#|PR-?)\d{3,}\b")

def rerank_recall(results, query, threshold=0.35, lex_weight=0.4):
    """Apply a relevance cutoff and an identifier-shaped lexical boost.
    Returns [] when nothing clears the cutoff (prompt recall injects nothing)."""
    q_tokens = set(re.findall(r"\w+", query.lower()))
    boosted = []
    for r in results:
        score = r.get("score", 0.0)
        lex = r.get("lexical_score", 0.0)
        text = r.get("text", "").lower()
        if SHA_RE.search(text) or TICKET_RE.search(text):   # commit SHA / ticket #N
            lex = max(lex, 1.0)
        fused = (1 - lex_weight) * score + lex_weight * lex
        if q_tokens and q_tokens <= set(text.split()):       # short id lookup bonus
            fused += 0.1
        boosted.append((fused, r))
    boosted.sort(reverse=True, key=lambda x: x[0])
    return [r for s, r in boosted if s >= threshold]

# kept = rerank_recall(recall_results, user_prompt, threshold=0.35)
# if kept: inject(kept)   # else inject nothing

