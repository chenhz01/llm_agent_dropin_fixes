# cline_workspace_pruner.py
# Source issue: https://github.com/cline/cline/issues/14682
# Upstream repo: cline/cline #14682
# Category: state_persist
# Root cause / claim: Prunes deleted folders from the persisted workspace list so the switcher stops showing dead entries (#14682).
# Verifier note: py filters workspaces by os.path.exists and reports pruned entries; maps to the stale-folder bug.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# cline_workspace_pruner.py
# For #14682: the workspace switcher list (key cline.code.workspace-selection.v2)
# keeps deleted folders because it's never validated against the filesystem.
# This prunes non-existent paths so the stale entry disappears.

import json, os

def prune(workspace_json):
    envs = workspace_json.get("environments", {})
    changed = False
    for env, cfg in envs.items():
        paths = cfg.get("workspaces", [])
        live = [p for p in paths if os.path.exists(p)]
        if len(live) != len(paths):
            changed = True
            cfg["workspaces"] = live
            if cfg.get("lastWorkspace") and not os.path.exists(cfg["lastWorkspace"]):
                cfg["lastWorkspace"] = live[-1] if live else None
    return workspace_json, changed

# --- paste the JSON extracted from the leveldb value here ---
raw = {
  "environments": {
    "local": {"lastWorkspace": "~/ai/ch32v203_iap",
              "workspaces": ["~/ai/ch32v203_iap",
                             "~/motor_driver_code"]}
  }
}
cleaned, changed = prune(raw)
print(json.dumps(cleaned, indent=2))
print("pruned stale entries:", changed)

