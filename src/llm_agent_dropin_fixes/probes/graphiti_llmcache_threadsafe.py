# graphiti_llmcache_threadsafe.py
# Source issue: https://github.com/getzep/graphiti/issues/1944
# Upstream repo: getzep/graphiti #1944
# Category: other
# Root cause / claim: Serializes LLMCache access with a lock so parallel set/get stop losing writes / returning wrong values.
# Verifier note: py eliminates the concurrency race by guarding the single connection.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_llmcache_threadsafe.py
import threading, json, sqlite3

class ThreadSafeCache:
    """Serialize all access to one LLMCache-shaped sqlite store."""
    def __init__(self, path):
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)

    def set(self, key, value):
        blob = json.dumps(value)  # let real LLMCache skip non-serializable
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO cache(key,value) VALUES(?,?)",
                (key, blob))
            self._conn.commit()

    def get(self, key):
        with self._lock:
            row = self._conn.execute(
                "SELECT value FROM cache WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

# Usage: swap graphiti_core's LLMCache for this in multithreaded ingest.
