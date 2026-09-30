# mem0_credential_suffix_probe.py
# Source issue: https://github.com/mem0ai/mem0/issues/7490
# Upstream repo: mem0ai/mem0 #7490
# Category: state_persist
# Root cause / claim: 突破组件：识别被 _credential 后缀误判为敏感而红化的非凭据字段（如 use_azure_credential 布尔开关），防止 AzureMySQLConfig 重建静默降级。
# Verifier note: py 针对 issue 7490 的 use_azure_credential 布尔开关场景，正确标出该字段会被误红化。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Catch bool / non-secret fields that _safe_deepcopy_config redacts only
# because they end in "_credential". Plug in your config fields + values.
SUFFIX = "_credential"

def over_redacted(fields: dict) -> list:
    """Fields matching the suffix but NOT actually a secret string."""
    bad = []
    for name, val in fields.items():
        if name.endswith(SUFFIX) and not isinstance(val, (str, bytes)):
            bad.append(name)
    return bad

if __name__ == "__main__":
    azure_mysql = {"connection_pool": "<live>", "use_azure_credential": True,
                   "host": "sql"}
    print(over_redacted(azure_mysql))   # ['use_azure_credential']
    # That bool is set to None on clone -> pydantic ValidationError and a
    # silent fallback to a plain object with no model_dump().

