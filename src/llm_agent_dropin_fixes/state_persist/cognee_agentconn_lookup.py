# cognee_agentconn_lookup.py
# Source issue: https://github.com/topoteretes/cognee/issues/4909
# Upstream repo: topoteretes/cognee #4909
# Category: state_persist
# Root cause / claim: 把按名查找改为 active_only=False 后再筛名，使已停用连接返回 status:inactive 而非 404，止住插件轮询报错。
# Verifier note: py 直接修正 issue 所述 active_only 预筛导致按名查找 404 的根因，可运行。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Correct lookup-by-name for agent connections. Plug in: replace the
# active_only=True + name-filter order in get_agent_connection_detail().

def get_connection_by_name(connections, agent_session_name):
    """Find one connection by name regardless of active state; activity is
    part of the answer, not a pre-filter (fixes the 404-on-deactivate bug)."""
    matches = [c for c in connections if c.get("agent_session_name") == agent_session_name]
    if not matches:
        return None  # genuinely unknown name -> 404 is correct here
    # Stable pick: prefer active, else the most recently updated inactive.
    matches.sort(key=lambda c: (c.get("status") != "active",
                                c.get("updated_at", "")))
    return matches[0]   # carries status: active|inactive for the caller

# all_conns = list_agent_connections(active_only=False)   # don't pre-drop inactive
# conn = get_connection_by_name(all_conns, "conn_x")
# -> returns {"agent_session_name": "conn_x", "status": "inactive"} instead of 404

