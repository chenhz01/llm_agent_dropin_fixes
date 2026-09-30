# li_refine_order_fix.py
# Source issue: https://github.com/run-llama/llama_index/issues/23155
# Upstream repo: run-llama/llama_index #23155
# Category: ctx_compact
# Root cause / claim: 以反向入队恢复 FIFO 顺序，修正 Refine 对重排子块的反向折叠。
# Verifier note: self-test：重入队后弹出顺序为 A,B,C，保持文档顺序，对应 #23155。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_refine_order_fix.py
# Fixes run-llama/llama_index#23155: Refine folds repacked sub-chunks in reverse document order.

from collections import deque

def requeue_subchunks(chunks_deque: deque, repacked: list):
    """Re-add sub-chunks WITHOUT reversing their document order (bug used extendleft)."""
    for sub in reversed(repacked):        # reversed push == FIFO restore
        chunks_deque.appendleft(sub)
    return chunks_deque

# --- self-test: document order [A,B,C] must be preserved ---
d = deque(["head"])
requeue_subchunks(d, ["A", "B", "C"])
print(list(d))   # ['A', 'B', 'C', 'head'] -> popped A,B,C in order
