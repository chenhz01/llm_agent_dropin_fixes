# graphiti_read_scope_resolver.py
# Source issue: https://github.com/getzep/graphiti/issues/1876
# Upstream repo: getzep/graphiti #1876
# Category: state_persist
# Root cause / claim: Derives the read driver from group_id like _resolve_request_scope, so reads follow the write's database.
# Verifier note: py returns the cloned db for reads matching the write scope.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_read_scope_resolver.py
def resolve_read_scope(group_ids, configured_db, driver_factory):
    """Derive the read driver from group_id, mirroring _resolve_request_scope.

    Today only add_episode calls _resolve_request_scope; reads skip it and
    hit `configured_db`, so cross-db reads return empty.
    """
    if not group_ids:
        return configured_db, driver_factory(configured_db)
    db = group_ids[0] if len(group_ids) == 1 else configured_db
    if db == configured_db:
        return db, driver_factory(configured_db)
    return db, driver_factory(db)        # same clone logic as writes

# Apply in Graphiti.search / get_episodes so reads follow the write's database.
