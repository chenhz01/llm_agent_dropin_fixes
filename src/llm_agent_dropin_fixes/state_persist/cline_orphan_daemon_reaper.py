# cline_orphan_daemon_reaper.py
# Source issue: https://github.com/cline/cline/issues/14700
# Upstream repo: cline/cline #14700
# Category: state_persist
# Root cause / claim: Detects orphaned remote-helper daemons re-parented to init, giving the hub a concrete reaper hook for the leak/OOM in #14700.
# Verifier note: py lists processes named cline-remote-helper with PPID==1 and their RSS; maps to the reported orphaned daemons.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# cline_orphan_daemon_reaper.py
# For #14700: finds leaked cline remote-helper daemons re-parented to PID 1
# (the OOM culprits) and prints safe kill commands.

import os, signal, sys

HELPER_MARK = "cline-remote-helper"

def find_orphans():
    out = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            stat = open(f"/proc/{pid}/stat").read().split()
            ppid = int(stat[3])
            name = stat[1].strip("()")
            if HELPER_MARK not in name:
                continue
            status = open(f"/proc/{pid}/status").read()
            rss_kb = int(status.split("VmRSS:")[1].split()[0])
            if ppid == 1:                  # healthy daemons are sidecar children
                out.append((int(pid), rss_kb))
        except (OSError, IndexError, ValueError):
            continue
    return out

if __name__ == "__main__":
    orphans = find_orphans()
    if not orphans:
        print("no orphaned helper daemons found")
        sys.exit(0)
    total_mb = sum(r for _, r in orphans) // 1024
    print(f"{len(orphans)} leaked daemon(s), ~{total_mb} MB held:")
    for pid, rss in orphans:
        print(f"  kill -TERM {pid}   # {rss//1024} MB")
    # dry-run by default; uncomment to actually reap:
    # for pid, _ in orphans: os.kill(pid, signal.SIGTERM)

