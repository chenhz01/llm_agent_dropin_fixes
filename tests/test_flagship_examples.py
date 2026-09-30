# -*- coding: utf-8 -*-
"""Flagship correctness tests — replay the bug, then prove the fix.

Four representative reference fixes are exercised end-to-end:
  1. cross-timezone history sort        (state_persist)
  2. Pinecone L2 distance -> similarity (memory_rerank)
  3. Pinecone filter translation        (rag_grounding)
  4. bounded-call hang guard            (loop_guard)

These use only the standard library, so they run without any optional deps.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from llm_agent_dropin_fixes.state_persist.mem0_history_resort import (
    resort_history, parse_ts,
)
from llm_agent_dropin_fixes.memory_rerank.mem0_pinecone_l2_rescore import (
    l2_to_similarity, rerank_euclidean,
)
from llm_agent_dropin_fixes.rag_grounding.mem0_pinecone_filter_fix import (
    to_pinecone_filter,
)
from llm_agent_dropin_fixes.loop_guard.gr_bounded_call_guard import bounded_call


# ---- 1. cross-timezone history sort (mem0 #7502) ----
def test_parse_ts_accepts_z_suffix():
    # Python <3.11 rejects a trailing 'Z'; the fix normalizes it.
    dt = parse_ts("2026-01-01T00:00:00Z")
    assert dt.utcoffset().total_seconds() == 0


def test_cross_timezone_resort_correct():
    events = [
        {"created_at": "2026-01-01T09:00:00+00:00", "event": "UPDATE"},
        {"created_at": "2026-01-01T10:00:00+08:00", "event": "ADD"},
    ]
    # Buggy baseline: lexicographic string sort puts UPDATE (UTC 09:00) first.
    raw = sorted(events, key=lambda e: e["created_at"])
    assert raw[0]["event"] == "UPDATE"
    # Fix: aware-datetime sort puts ADD (+08:00 == 01:00 UTC) first.
    fixed = resort_history(events)
    assert fixed[0]["event"] == "ADD"
    assert fixed[1]["event"] == "UPDATE"


# ---- 2. Pinecone L2 distance -> similarity (mem0 #7482) ----
def test_l2_to_similarity_endpoints():
    assert l2_to_similarity(0.0) == 1.0
    assert l2_to_similarity(4.0) == 0.2


def test_l2_to_similarity_monotonic():
    assert l2_to_similarity(0.0) > l2_to_similarity(1.0) > l2_to_similarity(4.0)


def test_rerank_euclidean_nearest_first():
    raw = [{"id": "far", "score": 4.0}, {"id": "near", "score": 0.0}]
    # Buggy baseline: distance treated as similarity -> 'far' ranks above 'near'.
    buggy = sorted(raw, key=lambda h: h["score"], reverse=True)
    assert buggy[0]["id"] == "far"
    # Fix: nearest (dist 0) listed first.
    fixed = rerank_euclidean(raw)
    assert fixed[0]["id"] == "near"
    assert fixed[-1]["id"] == "far"


# ---- 3. Pinecone filter translation (mem0 #7483) ----
def test_pinecone_filter_translation():
    bad = {"$or": [{"category": {"in": ["work"]}}, {"tag": {"eq": "x"}}]}
    out = to_pinecone_filter(bad)
    assert out == {
        "$or": [
            {"category": {"$in": ["work"]}},
            {"tag": {"$eq": "x"}},
        ]
    }


# ---- 4. bounded-call hang guard (gpt-researcher #1764) ----
def test_bounded_call_fast_returns_value():
    assert bounded_call(lambda: 42, timeout=5) == 42


def test_bounded_call_hang_raises_timeout():
    import pytest

    def hang():
        time.sleep(10)

    with pytest.raises(TimeoutError):
        bounded_call(hang, timeout=0.3, retries=2, backoff=0.1)
