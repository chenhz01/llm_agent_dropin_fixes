# flow_start_validator.py
# Source issue: https://github.com/crewAIInc/crewAI/issues/7758
# Upstream repo: crewAIInc/crewAI #7758
# Category: loop_guard
# Root cause / claim: Static validator that fails fast when a Flow has no @start() entrypoint, preventing the silent None return.
# Verifier note: Py inspects method sources for @start and raises before kickoff().
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import inspect

def assert_has_start(flow_cls):
    """Fail fast if a Flow has no @start() entrypoint (catches silent None)."""
    for name, _ in inspect.getmembers(flow_cls, predicate=callable):
        try:
            src = inspect.getsource(getattr(flow_cls, name))
        except (OSError, TypeError):
            continue
        if "@start" in src:
            return
    raise ValueError(
        f"{flow_cls.__name__} has no @start() method; kickoff() would "
        "silently return None. Add a @start() entrypoint."
    )

# Plug in your own Flow subclass
class MyFlow:
    pass

if __name__ == "__main__":
    assert_has_start(MyFlow)

