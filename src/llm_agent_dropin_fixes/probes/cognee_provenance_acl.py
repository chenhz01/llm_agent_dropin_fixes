# cognee_provenance_acl.py
# Source issue: https://github.com/topoteretes/cognee/issues/5110
# Upstream repo: topoteretes/cognee #5110
# Category: other
# Root cause / claim: 把 provenance 的数据集可见集改为按 ACL 授权计算，消除与 /visualize/brains 的口径分歧，修复空下拉。
# Verifier note: py 实现 issue 所述 ACL 授权可见集，与 owner/tenant 口径并集，直接对应空下拉根因。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Fix for provenance scoping: project the same readable set the rest of the
# multi-user API uses (ACL grants), not ownership.
# Plug in: replace the owner/tenant filter in GET /api/v1/schema/provenance/json
# with acl_readable_datasets().

def acl_readable_datasets(caller, all_datasets, grants):
    """Return dataset ids the caller can read via ACL, matching
    get_all_user_permission_datasets() used by /visualize/brains and /datasets.
    caller: {"user_id", "tenant_id"}; grants: list of
    {"dataset_id", "grantee_id", "grantee_tenant_id", "permission"}."""
    readable = set()
    for ds in all_datasets:
        if ds["owner_id"] == caller["user_id"]:
            readable.add(ds["id"]); continue
        if caller["tenant_id"] and ds["tenant_id"] == caller["tenant_id"]:
            readable.add(ds["id"]); continue
        for g in grants:
            if g["dataset_id"] != ds["id"]:
                continue
            granted = (g["grantee_id"] == caller["user_id"]
                       or (caller["tenant_id"]
                           and g["grantee_tenant_id"] == caller["tenant_id"]))
            if granted and g["permission"] in ("read", "write", "admin"):
                readable.add(ds["id"]); break
    return readable

# readable = acl_readable_datasets(caller, datasets, permission_grants)
# emit provenance Dataset nodes only for ids in readable

