# cline_reasoning_validator.py
# Source issue: https://github.com/cline/cline/issues/14649
# Upstream repo: cline/cline #14649
# Category: other
# Root cause / claim: Guards the reasoning level against each model's supported enum, preventing the Unsupported value commit-message error (#14649).
# Verifier note: py flags 'none' for gpt-6-astra as invalid and suggests 'medium'; matches the reported error.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# cline_reasoning_validator.py
# For #14649: commit generation passes reasoning="none" to gpt-6-astra, which
# only supports low/medium/high/xhigh/max -> Unsupported value error.
# Validate the level against the model's supported set before calling.

MODEL_REASONING = {
    "gpt-6-astra": ["low", "medium", "high", "xhigh", "max"],
    # add your own models here
}

def check(model, requested):
    supported = MODEL_REASONING.get(model)
    if supported is None:
        return f"unknown model {model!r}; verify its supported levels"
    if requested in supported:
        return f"OK: {requested} valid for {model}"
    fallback = "medium" if "medium" in supported else supported[0]
    return f"INVALID: {requested!r} not in {supported}; use {fallback}"

# --- plug your model + requested level here (no hardcoded secrets) ---
print(check("gpt-6-astra", "none"))    # -> INVALID, suggests medium
print(check("gpt-6-astra", "medium"))  # -> OK

