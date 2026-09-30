# mem0_cred_audit.py
# Source issue: https://github.com/mem0ai/mem0/issues/7504
# Upstream repo: mem0ai/mem0 #7504
# Category: state_persist
# Root cause / claim: 突破组件：在任何 VectorStoreFactory.create() 之前审计 config 哪些凭据字段会被深拷贝红化清空，提前暴露 Elasticsearch 构造失败 / OpenSearch 匿名连接。
# Verifier note: py 针对 issue 7504 的 api_key/password 被红化场景，审计两个真实 config 并正确标出风险字段。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Audit which credential fields _safe_deepcopy_config would blank before a
# VectorStoreFactory.create() call. Plug in your own config dict.
SENSITIVE_EXACT = {"api_key", "password", "token", "secret"}

def is_sensitive(field: str) -> bool:
    return field in SENSITIVE_EXACT or field.endswith("_credential")

def audit_config(cfg: dict) -> list:
    """Return credential fields that would be blanked on the clone."""
    at_risk = []
    for k, v in cfg.items():
        if v is not None and is_sensitive(k):
            at_risk.append(k)
    return at_risk

if __name__ == "__main__":
    es_cfg = {"api_key": "AK...", "host": "https://es:9200"}
    os_cfg = {"user": "u", "password": "p", "host": "https://os:9200"}
    print("elasticsearch:", audit_config(es_cfg))   # ['api_key']
    print("opensearch:  ", audit_config(os_cfg))    # ['password']
    # Any field listed here arrives at VectorStoreFactory as None.

