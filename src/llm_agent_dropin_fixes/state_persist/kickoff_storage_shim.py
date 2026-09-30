# kickoff_storage_shim.py
# Source issue: https://github.com/crewAIInc/crewAI/issues/7746
# Upstream repo: crewAIInc/crewAI #7746
# Category: state_persist
# Root cause / claim: Storage shim that serializes any JSON-able value on update and tolerates NULL on load, fixing the crash in KickoffTaskOutputsSQLiteStorage.
# Verifier note: Py patches update()/load() to match add() serialization and survive NULL fields.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import json
from crewai.memory.storage.kickoff_task_outputs_storage import (
    KickoffTaskOutputsSQLiteStorage,
)

_orig_update = KickoffTaskOutputsSQLiteStorage.update
_orig_load = KickoffTaskOutputsSQLiteStorage.load

def _safe_update(self, task_id, *a, **kw):
    for k, v in list(kw.items()):
        if not isinstance(v, (str, int, float, type(None))):
            kw[k] = json.dumps(v)  # list/dict -> str, like add()
    return _orig_update(self, task_id, *a, **kw)

def _safe_load(self, task_id):
    try:
        return _orig_load(self, task_id)
    except TypeError:
        return {"output": None, "inputs": None}  # tolerate NULL until row fixed

KickoffTaskOutputsSQLiteStorage.update = _safe_update
KickoffTaskOutputsSQLiteStorage.load = _safe_load

if __name__ == "__main__":
    print("safe storage shim installed")

