# graphiti_schema_require_all.py
# Source issue: https://github.com/getzep/graphiti/issues/1909
# Upstream repo: getzep/graphiti #1909
# Category: other
# Root cause / claim: Forces all json_schema properties required so grammar backends emit valid_at/invalid_at instead of omitting them.
# Verifier note: py makes optional date keys required in the sent schema.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_schema_require_all.py
def require_all_properties(model_json_schema: dict) -> dict:
    """Make every property required so grammar backends (llama.cpp/Ollama)
    emit valid_at/invalid_at instead of omitting optional keys.

    Input: the dict from pydantic model.model_json_schema().
    """
    props = model_json_schema.get("properties", {})
    patched = dict(model_json_schema)
    patched["required"] = list(props.keys())
    for name, sub in patched.get("$defs", {}).items():
        if isinstance(sub, dict) and "properties" in sub:
            sub["required"] = list(sub["properties"].keys())
    return patched

# Use in OpenAIGenericClient._build_response_format instead of the raw schema.
