"""Smoke gate: every fix module compiles (syntax-valid, drop-in ready).
Flagship modules have correctness tests in test_flagship_examples.py.
Per-fix bespoke assertion tests are welcome as PRs."""
import compileall, os, pytest
PKG_SRC = os.path.join(os.path.dirname(__file__), "..", "src", "llm_agent_dropin_fixes")

def _py_files():
    out = []
    for root, _, files in os.walk(PKG_SRC):
        for f in files:
            if f.endswith(".py"):
                out.append(os.path.join(root, f))
    return sorted(out)

def test_all_modules_compile():
    bad = [f for f in _py_files() if not compileall.compile_file(f, quiet=1)]
    assert not bad, f"compile failures: {bad}"
