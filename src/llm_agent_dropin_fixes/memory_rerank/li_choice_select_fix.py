# li_choice_select_fix.py
# Source issue: https://github.com/run-llama/llama_index/issues/23273
# Upstream repo: run-llama/llama_index #23273
# Category: memory_rerank
# Root cause / claim: 将 choice-select 解析收紧到 1..num_choices 的 1-based 边界，杜绝 0/负数静默指向末节点。
# Verifier note: self-test：num=0 被丢弃，num=2 正确返回索引 1，对应 #23273。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_choice_select_fix.py
# Fixes run-llama/llama_index#23273: non-positive choice numbers silently pick last node.
# (Complements your PR #23166 which fixes a different defect in the same fn.)

import re

def parse_choice_select(text: str, num_choices: int):
    """Return (valid_indices, relevances) with strict 1-based bounds [1, num_choices]."""
    nums, relevances = [], []
    for line in text.splitlines():
        m = re.search(r"answer_num:\s*(-?\d+).*?answer_relevance:\s*([\d.]+)", line)
        if not m:
            continue
        n = int(m.group(1))
        rel = float(m.group(2))
        if 1 <= n <= num_choices:        # drop 0 / negatives / out-of-range
            nums.append(n - 1)           # 0-based index
            relevances.append(rel)
    return nums, relevances

# --- self-test ---
print(parse_choice_select("answer_num: 0, answer_relevance: 9.5", 3))  # ([], []) -> dropped
print(parse_choice_select("answer_num: 2, answer_relevance: 9.5", 3))  # ([1], [9.5])
