# dify_dsl_dataset_audit.py
# Source issue: https://github.com/langgenius/dify/issues/43062
# Upstream repo: langgenius/dify #43062
# Category: memory_rerank
# Root cause / claim: Audits an imported workflow DSL for knowledge-retrieval nodes whose dataset_ids can't decrypt, converting a silent drop into a visible warning.
# Verifier note: py returns the undecodable (node_id, dataset_ids) pairs so the cross-workspace loss in #43062 is reported before import.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import json

# Pre-import check for workflow DSL: surface knowledge-retrieval nodes whose
# dataset_ids can't be decoded in the importing workspace, instead of importing
# 'successfully' with them silently dropped. Plug in your own decrypt + tenant id.

def audit_dsl(dsl_path, can_decrypt):
    with open(dsl_path) as f:
        dsl = json.load(f)
    lost = []
    for node in dsl.get('graph', {}).get('nodes', []):
        if node.get('data', {}).get('type') != 'knowledge-retrieval':
            continue
        ids = node['data']['config'].get('dataset_ids', [])
        bad = [i for i in ids if not can_decrypt(i)]
        if bad:
            lost.append((node['id'], bad))
    return lost  # list of (node_id, undecodable_dataset_ids)

if __name__ == '__main__':
    # lost = audit_dsl('exported.yml', lambda i: your_decrypt(i) is not None)
    # if lost: print('will drop datasets on import:', lost)
    pass
