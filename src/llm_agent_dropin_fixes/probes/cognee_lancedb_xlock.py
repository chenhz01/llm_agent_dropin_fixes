# cognee_lancedb_xlock.py
# Source issue: https://github.com/topoteretes/cognee/issues/5254
# Upstream repo: topoteretes/cognee #5254
# Category: other
# Root cause / claim: 跨进程 flock 把 LanceDB 的 create/merge_insert/delete 全量串行化，堵住 #5253 之外的跨进程写入竞争与重复向量 ID。
# Verifier note: py 提供跨进程 flock 串行化封装，直接覆盖 delete_data_points 未加锁的竞态（issue 真问题），可运行。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import os, fcntl, contextlib, time

# Cross-process serializer for local LanceDB mutations.
# Plug in: point the lock file next to your LanceDB store dir.
LOCK_DIR = os.path.expanduser("~/.cognee/lancedb")

@contextlib.contextmanager
def lancedb_write_lock(store_path, timeout=30.0):
    """Serialize all LanceDB mutations (create/merge_insert/delete) across
    processes sharing one store. Closes the gap where delete_data_points
    did not take VECTOR_DB_LOCK."""
    lock_path = os.path.join(store_path, ".cognee_write_lock")
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
    deadline = time.time() + timeout
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except BlockingIOError:
            if time.time() > deadline:
                raise TimeoutError("lancedb write lock timed out")
            time.sleep(0.1)
    try:
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)

# with lancedb_write_lock(store_path):
#     adapter.create_data_points(...)
#     adapter.delete_data_points(...)   # now races create/merge_insert safely

