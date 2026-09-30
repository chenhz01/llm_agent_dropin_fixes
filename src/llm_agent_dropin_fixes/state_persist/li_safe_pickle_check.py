# li_safe_pickle_check.py
# Source issue: https://github.com/run-llama/llama_index/issues/23256
# Upstream repo: run-llama/llama_index #23256
# Category: state_persist
# Root cause / claim: 在 persist 前校验对象是否落在上报允许清单，提前拒绝无法回载的对象。
# Verifier note: self-test：Report 实例被报告为不可持久化，对应 #23256。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_safe_pickle_check.py
# Fixes run-llama/llama_index#23256: persist() writes files from_persist_dir can't load.
# Companion to the CWE-502 hardening in #20857: refuse up front when loader will reject.

_SAFE = (str, int, float, bool, type(None), tuple, list, dict, set, bytes)

def check_persistable(objs) -> list:
    """Return the names of classes in `objs` that _RestrictedUnpickler will reject."""
    bad = []
    for o in objs:
        t = type(o)
        if t not in _SAFE:
            bad.append(f"{t.__module__}.{t.__name__}")
    return bad

# --- self-test ---
class Report:
    pass
print(check_persistable(["ok", Report()]))   # ['__main__.Report'] -> persist() should refuse
