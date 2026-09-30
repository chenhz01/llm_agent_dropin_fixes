# li_prevnext_score_fix.py
# Source issue: https://github.com/run-llama/llama_index/issues/23199
# Upstream repo: run-llama/llama_index #23199
# Category: memory_rerank
# Root cause / claim: 在邻居扩展后保留原始检索分数，防止 PrevNextNodePostprocessor 把已知分数覆盖成 None。
# Verifier note: self-test：扩展后 b 的 score 由 None 恢复为 0.9，对应 #23199。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_prevnext_score_fix.py
# Fixes run-llama/llama_index#23199: neighbor expansion drops original retrieval scores.
# Drop-in wrapper around PrevNextNodePostprocessor that keeps each node's best known score.

from llama_index.core.schema import NodeWithScore

def preserve_scores(retrieved, expanded):
    """expanded: postprocessor output; restore any score we already knew from `retrieved`."""
    known = {n.node.node_id: n.score for n in retrieved}
    out = []
    for n in expanded:
        score = n.score
        if score is None and n.node.node_id in known:
            score = known[n.node.node_id]
        out.append(NodeWithScore(node=n.node, score=score))
    return out

# --- self-test ---
a = NodeWithScore(node=type("N", (), {"node_id": "a"})(), score=0.8)
b = NodeWithScore(node=type("N", (), {"node_id": "b"})(), score=0.9)
expanded = [NodeWithScore(node=type("N", (), {"node_id": "b"})(), score=None)]
fixed = preserve_scores([a, b], expanded)
print([(n.node.node_id, n.score) for n in fixed])  # [('b', 0.9)] score restored
