# lc_tool_call_accumulator.py
# Source issue: https://github.com/langchain-ai/langchain/issues/40826
# Upstream repo: langchain-ai/langchain #40826
# Category: other
# Root cause / claim: Buffers streamed tool-call argument deltas and parses the full JSON once, removing the per-chunk O(n^2) re-parse.
# Verifier note: py accumulates all deltas then parses a single time; directly addresses the repeated re-parse cost in #40826.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# lc_tool_call_accumulator.py
# Fixes #40826: large streamed tool calls re-parse args on every chunk.
# Buffer deltas and JSON-parse the full payload once when the object closes.
import json

def accumulate_tool_args(chunks):
    """Join streamed arg deltas and JSON-parse once when the object completes."""
    buf, depth, started = [], 0, False
    for delta in chunks:
        buf.append(delta)
        for ch in delta:
            if ch == "{":
                depth += 1; started = True
            elif ch == "}":
                depth -= 1
    if not started:
        return {}
    return json.loads("".join(buf))  # parsed a single time, not per chunk

# Collect AIMessageChunk tool_call argument fragments, then call once:
# args = accumulate_tool_args(fragments)
