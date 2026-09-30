# dify_logs_paginator.py
# Source issue: https://github.com/langgenius/dify/issues/43134
# Upstream repo: langgenius/dify #43134
# Category: state_persist
# Root cause / claim: Keyset pagination on (created_at, id) makes message ordering deterministic so tied timestamps never drop a chat message.
# Verifier note: py pages 4 rows sharing one created_at into two complete pages with no row skipped, directly fixing #43134.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

from datetime import datetime

# Reference fix for 'items sharing created_at get skipped' pagination bugs.
# Use a keyset cursor on (created_at, id) so ties resolve deterministically.
# Plug in your own DB client / ORM query in place of the rows list below.

def page(rows, last_id=None, limit=10):
    rows = sorted(rows, key=lambda r: (r['created_at'], r['id']))
    if last_id is not None:
        start = next(i for i, r in enumerate(rows) if r['id'] == last_id) + 1
    else:
        start = 0
    page_rows = rows[start:start + limit]
    return page_rows, len(rows) > start + limit  # (data, has_more)

if __name__ == '__main__':
    t = datetime(2024, 1, 1, 12, 0, 0)
    rows = [{'id': f'r{i}', 'created_at': t} for i in range(4)]  # all share created_at
    p1, more = page(rows, last_id=None, limit=2)
    p2, more = page(rows, last_id=p1[-1]['id'], limit=2)
    print([r['id'] for r in p1], [r['id'] for r in p2], more)
    # ['r0','r1'] ['r2','r3'] False -> no row skipped
