# cline_session_time_auditor.py
# Source issue: https://github.com/cline/cline/issues/14642
# Upstream repo: cline/cline #14642
# Category: state_persist
# Root cause / claim: Flags sessions whose updatedAt resets to 'now' on launch without new activity, pinpointing the phantom-timestamp bug (#14642).
# Verifier note: py flags a session whose updatedAt ~ launch but lastMessageAt is a day old; reproduces the 'now' symptom.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# cline_session_time_auditor.py
# For #14642: some sessions show "now" after a restart with no real activity.
# Flag entries whose updatedAt is implausibly fresh vs their last message.

import time

GRACE_S = 30  # touched within this of launch with no new msg = suspicious

def audit(sessions, launch_ts=None):
    launch_ts = launch_ts or time.time()
    suspect = []
    for s in sessions:
        up = s.get("updatedAt", 0)
        up = up / 1000.0 if up > 1e12 else up      # ms->s if needed
        last = s.get("lastMessageAt", 0)
        last = last / 1000.0 if last > 1e12 else last
        fresh = (launch_ts - up) < GRACE_S
        no_activity = last and abs(up - last) < 1   # bumped with no new msg
        if fresh and no_activity:
            suspect.append(s.get("id"))
    return suspect

# --- load your sessions.json here (no secrets needed) ---
sessions = [{"id": "A", "updatedAt": int(time.time()*1000),
             "lastMessageAt": int((time.time()-86400)*1000)}]
print("suspect 'now' sessions:", audit(sessions))

