# cognee_triplet_backfill.py
# Source issue: https://github.com/topoteretes/cognee/issues/4822
# Upstream repo: topoteretes/cognee #4822
# Category: memory_rerank
# Root cause / claim: 从端点节点的 node_map 回填 belongs_to_set 到 Triplet/EdgeType 载荷，修复 node-set 过滤 triplet 检索恒为空 + 全表扫描。
# Verifier note: py 针对 issue 所述 0/N 携带 belongs_to_set、过滤检索恒空的缺陷，做探测+回填，可运行。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Repair + probe for missing belongs_to_set on Triplet/EdgeType datapoints.
# Plug in: run once against your vector store to backfill tags from node_map,
# then keep the upstream fix (propagate tags in _create_triplets_from_graph).

def detect_missing(collection):
    """Probe: how many payloads lack belongs_to_set."""
    empty = 0
    for doc in collection.get_all():   # your vector client's iterator
        if not doc.payload.get("belongs_to_set"):
            empty += 1
    return empty

def backfill(collection, node_tags):
    """Set belongs_to_set on each triplet/edge payload from its endpoint nodes.
    node_tags: {node_id: ["set_a", "set_b"]} built from node_map."""
    updated = 0
    for doc in collection.get_all():
        tags = set()
        for nid in (doc.payload.get("from_node_id"),
                    doc.payload.get("to_node_id")):
            tags.update(node_tags.get(nid, []))
        doc.payload["belongs_to_set"] = sorted(tags)
        collection.update(doc.id, payload=doc.payload)
        updated += 1
    return updated

# if detect_missing(triplet_collection): backfill(triplet_collection, node_tags)

