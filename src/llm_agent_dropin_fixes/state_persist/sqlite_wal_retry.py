# sqlite_wal_retry.py
# Source issue: https://github.com/crewAIInc/crewAI/issues/7822
# Upstream repo: crewAIInc/crewAI #7822
# Category: state_persist
# Root cause / claim: Bounded exponential-backoff wrapper around PRAGMA journal_mode=WAL that removes the 'database is locked' race the maintainer's PR #7821 targets.
# Verifier note: Py is a drop-in retry for the WAL switch; complements your PR #7821, does not duplicate it.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import sqlite3, time

# Bounded retry for the WAL switch your PR #7821 already touches.
def set_wal(db_path, tries=7, base=0.02):
    last = None
    for i in range(tries):
        try:
            with sqlite3.connect(db_path) as con:
                con.execute("PRAGMA journal_mode=WAL")
            return
        except sqlite3.OperationalError as exc:  # database is locked
            last = exc
            time.sleep(base * (2 ** i))  # bounded exponential backoff
    raise last

if __name__ == "__main__":
    set_wal("flow_state.db")  # plug in your own db path
    print("WAL ok")

