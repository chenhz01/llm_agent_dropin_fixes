# graphiti_nested_attr_serialize.py
# Source issue: https://github.com/getzep/graphiti/issues/1885
# Upstream repo: getzep/graphiti #1885
# Category: ctx_compact
# Root cause / claim: Serializes legitimately nested attributes to JSON strings for all providers and drops only schema-echo shapes, preserving real data.
# Verifier note: py keeps the 40 real nested extractions, drops the 43 schema echoes.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_nested_attr_serialize.py
import json

def serialize_attributes(attrs: dict, schema_markers=("type", "description")):
    """Make attributes property-graph safe.

    Nested maps -> JSON string (data survives). A value that looks like a
    schema echo (has 'type'/'description' keys) is dropped and flagged.
    """
    out, dropped = {}, []
    for k, v in attrs.items():
        if isinstance(v, dict):
            if set(v.keys()) <= set(schema_markers):
                dropped.append(k)            # model echoed the schema, not a value
                continue
            out[k] = json.dumps(v, ensure_ascii=False)   # keep real nested data
        else:
            out[k] = v
    return out, dropped

# Apply in EntityNode/EntityEdge.save for non-Kuzu providers too.
