# mem0_orphan_msgs_audit.py
# Source issue: https://github.com/mem0ai/mem0/issues/7452
# Upstream repo: mem0ai/mem0 #7452
# Category: state_persist
# Root cause / claim: 突破组件：量化 delete_all() 之后残留的会话消息条数，定位会被下次 add() 重新喂给 LLM 并复提取的数据残留。
# Verifier note: py 针对 issue 7452 直接查询 messages 表，标出某 scope 在 delete_all 后仍残留的会话消息数。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# After delete_all(user_id="alice"), her recent session messages stay in the
# history DB and get re-fed to the LLM on the next add(). Audit the leak.
# Plug in your own history_db_path.
import sqlite3

def orphaned_messages(db_path: str, scope: str) -> int:
    con = sqlite3.connect(db_path)
    try:
        cur = con.execute(
            "SELECT COUNT(*) FROM messages WHERE session_scope = ?", (scope,)
        )
        return cur.fetchone()[0]
    finally:
        con.close()

if __name__ == "__main__":
    n = orphaned_messages("/path/to/history.db", "user_id:alice")
    print(f"{n} session messages survive delete_all -> re-sent on next add()")
    # Pair with a delete_messages(session_scope) on SQLiteManager to clear them.

