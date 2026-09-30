# graphiti_mcp_scope_expand.py
# Source issue: https://github.com/getzep/graphiti/issues/1919
# Upstream repo: getzep/graphiti #1919
# Category: other
# Root cause / claim: Expands '*' to all groups and reports the searched scope so empty results aren't misread as 'no data'.
# Verifier note: py returns all groups for '*' and labels the scope.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_mcp_scope_expand.py
ALL = "*"

def resolve_scope(group_ids, known_groups, default):
    """Expand '*' to every group and report the scope actually searched.

    Returns (resolved_group_ids, scope_label).
    Fail-closed: missing/empty -> default, never cross-tenant implicitly.
    """
    if group_ids is None or group_ids == []:
        return [default], f"default:{default}"
    if ALL in group_ids:
        return list(known_groups), f"all:{len(known_groups)}"
    return group_ids, f"groups:{group_ids}"

# In the tool response, echo scope_label so an empty result reads as
# "nothing in <scope>" rather than "nothing at all".
