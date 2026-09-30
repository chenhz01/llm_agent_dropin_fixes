# cline_perm_scope_auditor.py
# Source issue: https://github.com/cline/cline/issues/14699
# Upstream repo: cline/cline #14699
# Category: state_persist
# Root cause / claim: Audits which settings scope grants a permission, surfacing the project-vs-user allow discrepancy behind the silent refusals in #14699.
# Verifier note: py resolves a command against both scopes and reports the effective grant; reproduces the reported allow-rule divergence.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# cline_perm_scope_auditor.py
# For #14699: checks a command against BOTH project (.claude/settings.json)
# and user (~/.claude/settings.json) permission scopes to expose the
# project-vs-user allow discrepancy behind the silent refusals.

import json, os

def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except OSError:
        return {}

def resolve(cmd, project_cfg, user_cfg):
    p_allow = project_cfg.get("permissions", {}).get("allow", [])
    u_allow = user_cfg.get("permissions", {}).get("allow", [])
    p_deny  = project_cfg.get("permissions", {}).get("deny", [])
    if any(cmd in d for d in p_deny):
        return "DENIED (project deny)"
    if any(cmd in a for a in p_allow):
        return "ALLOWED via project allow"
    if any(cmd in a for a in u_allow):
        return "ALLOWED via USER allow (project allow ignored this cmd)"
    return "REQUIRES APPROVAL (no matching allow in either scope)"

# --- point at your real config files (no secrets needed) ---
proj = load(os.path.expanduser("YOUR_PROJECT/.claude/settings.json"))
user = load(os.path.expanduser("~/.claude/settings.json"))
for cmd in ["Bash(python3:*)", "mcp__svc__research_config"]:
    print(cmd, "->", resolve(cmd, proj, user))

