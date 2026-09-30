# graphiti_llmcache_circular_safe.py
# Source issue: https://github.com/getzep/graphiti/issues/1942
# Upstream repo: getzep/graphiti #1942
# Category: other
# Root cause / claim: Catches ValueError (circular refs) in LLMCache.set so non-serializable values are skipped like TypeError cases.
# Verifier note: py skips circular refs instead of raising.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_llmcache_circular_safe.py
import json, logging

log = logging.getLogger("llmcache")

def safe_set(cache, key, value):
    """Drop non-JSON-serializable values (circular refs too) instead of raising."""
    try:
        serialized = json.dumps(value)
    except (TypeError, ValueError) as e:  # circular -> ValueError
        log.warning("Non-JSON-serializable cache value for key %s, skipping: %s", key, e)
        return None
    return cache._store(key, serialized)  # plug in your cache store call

# Equivalent one-line patch for graphiti_core/llm_client/cache.py:
# except (TypeError, ValueError):
