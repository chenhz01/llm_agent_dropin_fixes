# graphiti_mcp_arg_linter.py
# Source issue: https://github.com/getzep/graphiti/issues/1932
# Upstream repo: getzep/graphiti #1932
# Category: other
# Root cause / claim: Validates MCP tool args against the declared schema and suggests the closest valid name for misspellings like group_id/group_ids.
# Verifier note: py catches unknown/misspelled arg before it is silently dropped.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_mcp_arg_linter.py
from difflib import get_close_matches

def lint_tool_args(model, supplied: dict):
    """Warn on unknown keys and suggest the closest declared arg.

    model: pydantic model class for the MCP tool (e.g. SearchNodes).
    supplied: raw kwargs the client sent.
    """
    declared = set(model.model_fields.keys())
    warnings = []
    for k in supplied:
        if k not in declared:
            near = get_close_matches(k, declared, n=1)
            hint = f" did you mean '{near[0]}'?" if near else ""
            warnings.append(f"unknown arg '{k}'{hint} (will be dropped)")
    return warnings

# Usage before the tool body:
# ws = lint_tool_args(SearchNodes, {"query":"x","group_id":"p"})
# if ws: raise ValueError("; ".join(ws))   # fail closed, name the bad arg
