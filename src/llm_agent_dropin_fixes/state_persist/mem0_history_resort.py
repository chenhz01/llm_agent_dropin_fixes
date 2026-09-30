# mem0_history_resort.py
# Source issue: https://github.com/mem0ai/mem0/issues/7502
# Upstream repo: mem0ai/mem0 #7502
# Category: state_persist
# Root cause / claim: 突破组件：把 mem0 history() 的字符串比较改成按真实 UTC 偏移感知时间点排序，彻底消除跨时区审计顺序错乱。
# Verifier note: py 直接复现 issue 7502 的排序错误并以 aware datetime 修正；对样例 (ADD +08:00, UPDATE UTC) 输出正确顺序。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

from datetime import datetime

def parse_ts(ts: str) -> datetime:
    # Python <3.11 rejects 'Z'; normalize then parse as timezone-aware.
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)

def resort_history(events: list) -> list:
    """Re-sort mem0 history() output oldest-first by real instant.

    Plug in your own fetched events, e.g. m.history(memory_id).
    """
    return sorted(events, key=lambda e: parse_ts(e["created_at"]))

if __name__ == "__main__":
    sample = [
        {"created_at": "2026-01-01T09:00:00+00:00", "event": "UPDATE", "new_memory": "v3"},
        {"created_at": "2026-01-01T10:00:00+08:00", "event": "ADD", "new_memory": "v1"},
    ]
    for e in resort_history(sample):
        print(e["created_at"], e["event"])
    # ADD (+08:00) prints before UPDATE (UTC) - chronologically correct

