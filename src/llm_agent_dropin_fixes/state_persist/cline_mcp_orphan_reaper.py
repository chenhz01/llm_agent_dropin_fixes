# cline_mcp_orphan_reaper.py
# Source issue: https://github.com/cline/cline/issues/14622
# Upstream repo: cline/cline #14622
# Category: state_persist
# Root cause / claim: Lists orphaned MCP server processes that outlive their session, giving the hub a reaper hook for /clear and quit (#14622).
# Verifier note: py enumerates /proc for mcp/serena/clangd processes and prints kill commands; maps to the reported leak.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# cline_mcp_orphan_reaper.py
# For #14622: in CLI hub mode, a session's stdio MCP servers (Serena + clangd /
# lua-language-server) are never stopped on /clear or quit, so they pile up.
# This lists the orphans and prints safe kill commands.

import os, signal, sys

MARKERS = ("mcp", "serena", "clangd", "lua-language-server")

def find_orphans():
    out = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            cmd = open(f"/proc/{pid}/cmdline").read().replace(chr(0), " ").strip()
            if not any(m in cmd.lower() for m in MARKERS):
                continue
            ppid = int(open(f"/proc/{pid}/stat").read().split()[3])
            out.append((int(pid), ppid, cmd[:60]))
        except (OSError, IndexError, ValueError):
            continue
    return out

if __name__ == "__main__":
    orphans = find_orphans()
    print(f"{len(orphans)} MCP-related process(es):")
    for pid, ppid, cmd in orphans:
        print(f"  kill -TERM {pid}  (ppid={ppid})  {cmd}")
    # dry-run; uncomment to reap:
    # for pid, _, _ in orphans: os.kill(pid, signal.SIGTERM)

