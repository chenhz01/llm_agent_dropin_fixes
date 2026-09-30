# graphiti_max_tokens_resolve.py
# Source issue: https://github.com/getzep/graphiti/issues/1869
# Upstream repo: getzep/graphiti #1869
# Category: ctx_compact
# Root cause / claim: Consults the model's real output budget for extract_edges instead of the hard-coded 16384 cap.
# Verifier note: py returns 65536 for gemini-2.5-flash unless caller asks lower.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_max_tokens_resolve.py
GEMINI_MAX = {"gemini-2.5-flash": 65536, "gemini-2.5-pro": 65536}
OPENAI_MAX = {"gpt-4o": 16384}

def resolve_max_tokens(explicit, model, provider):
    """Use the model's real output budget unless the caller asks for less."""
    table = GEMINI_MAX if provider == "gemini" else OPENAI_MAX
    model_cap = table.get(model)
    if explicit is not None:
        if model_cap and explicit > model_cap:
            raise ValueError(
                f"max_tokens {explicit} exceeds {model} cap {model_cap}")
        return explicit
    return model_cap   # don't silently quarter a 65k-capable model

# Plug into extract_edges so Gemini 2.5 gets its full 65536 budget.
