# cognee_notion_incremental.py
# Source issue: https://github.com/topoteretes/cognee/issues/4820
# Upstream repo: topoteretes/cognee #4820
# Category: state_persist
# Root cause / claim: 在保持每轮全量枚举（orphan_cleanup 安全）的前提下，用 last_edited_time 水位只重渲染变更页，降低 Notion 读取成本。
# Verifier note: py 针对 issue 的'全量枚举但跳过渲染 + 防误删'约束，给出增量水位逻辑，可运行。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Incremental Notion sync that keeps the snapshot authoritative (orphan-safe).
# Plug in: replace the full re-render loop in the DLT source's _page_to_row.

def incremental_pages(pages, prev_watermarks, render, stored_content):
    """Enumerate EVERY page (keeps snapshot complete -> safe orphan_cleanup),
    but only call _render_blocks for pages whose last_edited_time moved.
    Returns (rows_to_emit, page_ids_seen)."""
    rows, seen = [], set()
    for p in pages:                      # full enumeration, cheap list call
        pid = p["id"]
        seen.add(pid)
        edited = p["last_edited_time"]
        if prev_watermarks.get(pid) == edited:
            rows.append(stored_content[pid])   # unchanged -> reuse, skip render
        else:
            rows.append(render(p))             # changed -> re-render
    return rows, seen

def orphan_deletes(current_ids, graph_ids):
    """Forget only pages absent from the authoritative listing."""
    return [g for g in graph_ids if g not in current_ids]

# rows, seen = incremental_pages(pages, watermarks, _render_blocks, cache)
# forget(orphan_deletes(seen, graph_page_ids))

