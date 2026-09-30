# cognee_conn_badge_merge.py
# Source issue: https://github.com/topoteretes/cognee/issues/4957
# Upstream repo: topoteretes/cognee #4957
# Category: state_persist
# Root cause / claim: 把活跃注册连接（connections?active_only=true）并入连接状态判定，使新连接在无 session 行时立即显示 Connected。
# Verifier note: py 针对 issue 所述'活跃连接但无 session 行仍显示 Connect'现象，补充连接态合并，可运行。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Merge session-derived and connection-derived "connected" state for the
# integrations UI. Plug in: compute the badge in the dashboard data layer.

RECOGNIZED_PREFIXES = ("claude", "codex", "cursor", "gemini")

def integration_connected(integration, sessions, connections):
    """Return True if the integration should show 'Connected'.
    Prefers an active registered connection; falls back to session rows."""
    sid = integration.get("session_id", "") or integration.get("id", "")
    prefix = next((p for p in RECOGNIZED_PREFIXES if sid.startswith(p)), None)
    # 1) Active registered connection wins immediately (no session needed).
    for c in connections:
        if c.get("active") and c.get("session_id", "").startswith(prefix or sid):
            return True
    # 2) Fallback: existing session-derived detection.
    for s in sessions:
        if s.get("session_id", "").startswith(prefix or sid):
            return True
    return False

# for card in integration_cards:
#     card["connected"] = integration_connected(card, sessions, connections)

