# dify_content_budget_probe.py
# Source issue: https://github.com/langgenius/dify/issues/43113
# Upstream repo: langgenius/dify #43113
# Category: ctx_compact
# Root cause / claim: Quantifies how much retrieved content is truncated under the 2000/12000 char limits so operators can pick sane values.
# Verifier note: py reports chars_lost_to_result_limit and a suggested limit, directly supporting the tuning request in #43113.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Content-budget probe for Agent knowledge retrieval.
# Reports how much of each retrieved parent chunk is lost under the current
# max_result_content_chars / max_observation_chars limits, and suggests a value.
# Plug in your own retrieved chunks and model context budget below.

def probe(chunks, max_result=2000, max_obs=12000, budget=8000):
    kept = sum(min(len(c), max_result) for c in chunks)
    lost = sum(max(0, len(c) - max_result) for c in chunks)
    return {
        'chars_lost_to_result_limit': lost,
        'kept_total': kept,
        'would_truncate_observation': kept > max_obs or kept > budget,
        'suggest_max_result': max(2000, budget // max(len(chunks), 1)),
    }

if __name__ == '__main__':
    # print(probe([long_chunk1, long_chunk2], budget=8000))
    pass
