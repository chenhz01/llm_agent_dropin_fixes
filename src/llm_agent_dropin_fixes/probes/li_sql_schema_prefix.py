# li_sql_schema_prefix.py
# Source issue: https://github.com/run-llama/llama_index/issues/23301
# Upstream repo: run-llama/llama_index #23301
# Category: other
# Root cause / claim: 对 SQL 字面量与注释先做掩码再仅对真实表引用加 schema 前缀，避免 FROM/JOIN 文本被改写。
# Verifier note: self-test 显示字面量 'FROM users' 与注释不被改写，输出 tenant.users 仅在真实表引用处。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_sql_schema_prefix.py
# Fixes run-llama/llama_index#23301: schema prefix bleeds into SQL string literals/comments.

import re

def _mask(sql: str):
    store = []
    pat = re.compile(r"'(?:[^']|'')*'|--[^\n]*|/\*.*?\*/", re.S)
    def sub(m):
        store.append(m.group(0))
        return f"\x00{len(store) - 1}\x00"
    return pat.sub(sub, sql), store

def add_schema_prefix(sql: str, schema: str) -> str:
    masked, store = _mask(sql)
    def repl(m):
        kw, tbl = m.group(1), m.group(2)
        return f"{kw} {schema}.{tbl}" if "." not in tbl else m.group(0)
    fixed = re.sub(r"\b(FROM|JOIN)\s+([A-Za-z_]\w*)\b", repl, masked, flags=re.I)
    for i, s in enumerate(store):
        fixed = fixed.replace(f"\x00{i}\x00", s)
    return fixed

# --- self-test ---
sql = "SELECT 'FROM users', name FROM users -- JOIN ignored"
print(add_schema_prefix(sql, "tenant"))  # -> SELECT 'FROM users', name FROM tenant.users -- JOIN ignored
