# max_iter_guard.py
# Source issue: https://github.com/crewAIInc/crewAI/issues/7757
# Upstream repo: crewAIInc/crewAI #7757
# Category: loop_guard
# Root cause / claim: Constructor guard that rejects max_iter < 1, turning the nonsense RecursionError into a clear validation error.
# Verifier note: Py blocks max_iter=0 at Agent() construction, matching the issue's expected behavior.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

from crewai import Agent

_base_init = Agent.__init__

def _guarded_init(self, *args, **kwargs):
    mi = kwargs.get("max_iter", getattr(self, "max_iter", None))
    if mi is not None and mi < 1:
        raise ValueError(
            f"max_iter must be >= 1 (got {mi}); 0/negative mislead the loop "
            "detector into a RecursionError. Use max_iter=1 for one pass."
        )
    _base_init(self, *args, **kwargs)

Agent.__init__ = _guarded_init  # install before constructing agents

if __name__ == "__main__":
    try:
        Agent(role="a", goal="b", backstory="c", max_iter=0)
    except ValueError as e:
        print("blocked:", e)

