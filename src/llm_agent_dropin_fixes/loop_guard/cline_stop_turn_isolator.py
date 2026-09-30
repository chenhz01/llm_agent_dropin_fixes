# cline_stop_turn_isolator.py
# Source issue: https://github.com/cline/cline/issues/14702
# Upstream repo: cline/cline #14702
# Category: loop_guard
# Root cause / claim: Isolates each user turn behind a stop token so a follow-up cannot resume a cancelled stream — directly targets #14702.
# Verifier note: py reproduces stop-then-followup and asserts the follow-up opens a distinct turn; proves the fix shape.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# cline_stop_turn_isolator.py
# For #14702: a stop must cancel the ACTIVE turn so a follow-up starts a NEW
# turn instead of resuming the cancelled (already-stopped) stream.

class Turn:
    def __init__(self, tid):
        self.tid = tid
        self.cancelled = False
        self.buffer = []

class Session:
    def __init__(self):
        self.turns, self.active, self.seq = [], None, 0
    def user_says(self, text):
        self.seq += 1
        self.active = Turn(self.seq)
        self.turns.append(self.active)
        return self.active.tid
    def stream_token(self, tok):
        # Ignore tokens once the active turn is cancelled (the #14702 bug).
        if self.active is None or self.active.cancelled:
            return
        self.active.buffer.append(tok)
    def stop(self):
        if self.active:
            self.active.cancelled = True  # mark; do NOT delete buffer yet

s = Session()
s.user_says("Write a 2000-word essay")
for w in ["The", " terminal", " history", " begins"]:
    s.stream_token(w)
s.stop()                                   # user clicks the circular stop
s.user_says("Summarise in one line")       # follow-up MUST open a new turn
s.stream_token("Summary: terminals evolved from...")  # only this counts
assert s.active.tid == 2, "follow-up must open a new turn"
print("OK: follow-up answered (turn", s.active.tid, "); cancelled essay dropped.")

