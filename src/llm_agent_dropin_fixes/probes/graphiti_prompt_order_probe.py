# graphiti_prompt_order_probe.py
# Source issue: https://github.com/getzep/graphiti/issues/1931
# Upstream repo: getzep/graphiti #1931
# Category: other
# Root cause / claim: Diffs add_episode prompt output across PYTHONHASHSEED values to catch non-deterministic ordering regressions.
# Verifier note: py fails when set/db-order lists diverge across seeds.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_prompt_order_probe.py
import os, subprocess, sys, difflib

def stable_across_seeds(build_prompt, seeds=(0, 1, 2)):
    """Re-run build_prompt under different PYTHONHASHSEED and compare output.

    build_prompt: callable returning the prompt string for one episode.
    Returns (is_stable, diffs).
    """
    outputs = {}
    for s in seeds:
        env = {**os.environ, "PYTHONHASHSEED": str(s)}
        out = subprocess.run([sys.executable, "-c",
            "import runpy,sys; sys.path.insert(0,'.'); "
            "print(build_prompt())"],
            capture_output=True, text=True, env=env)
        outputs[s] = out.stdout
    keys = list(outputs)
    diffs = [d for k in keys[1:] for d in difflib.unified_diff(
        outputs[keys[0]].splitlines(), outputs[k].splitlines())]
    return (len(diffs) == 0), diffs

# Plug build_prompt with your add_episode prompt builder to catch 1931 regressions.
