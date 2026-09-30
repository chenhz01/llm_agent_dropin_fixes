# li_dup_format_detect.py
# Source issue: https://github.com/run-llama/llama_index/issues/23267
# Upstream repo: run-llama/llama_index #23267
# Category: token_guard
# Root cause / claim: 检测 prompt 中重复出现的 format 块，作为回归守卫捕捉多选提示被重复注入。
# Verifier note: self-test：good 返回 False、bad 返回 True，对应 #23267。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_dup_format_detect.py
# Fixes run-llama/llama_index#23267: multi-select prompt ships the format block twice.
# (Your PR adds the regression test; this is a standalone lint you can run in CI.)

def count_format_block(prompt: str, marker: str = "Here is an example") -> int:
    """Return how many times the JSON format block appears; expect <= 1."""
    return prompt.count(marker)

def has_duplicate_format(prompt: str) -> bool:
    return count_format_block(prompt) > 1

# --- self-test ---
good = 'The output should be ONLY JSON formatted. Here is an example: [...]'
bad = good + ' The output should be ONLY JSON formatted. Here is an example: [...]'
print(has_duplicate_format(good))   # False
print(has_duplicate_format(bad))    # True
