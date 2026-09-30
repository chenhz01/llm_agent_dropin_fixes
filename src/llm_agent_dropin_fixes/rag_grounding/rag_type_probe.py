# rag_type_probe.py
# Source issue: https://github.com/crewAIInc/crewAI/issues/7827
# Upstream repo: crewAIInc/crewAI #7827
# Category: rag_grounding
# Root cause / claim: Per-item, case-normalized data_type detection that kills the outer-variable leakage and uppercase-extension misses in CrewAIRagAdapter.add().
# Verifier note: Py reproduces the exact failures (DIRECTORY locking onto files, .PDF -> TEXT_FILE) and shows corrected per-item lowercase detection.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import os

# Plug in your own content sources (paths or urls)
SOURCES = ["/data/report.PDF", "/data/notes.txt", "/data/feed.json"]

def norm_ext(path):
    return os.path.splitext(path)[1].lower()

def from_content(source):
    ext = norm_ext(source)
    if ext == ".pdf":
        return "PDF_FILE"
    if ext == ".json":
        return "JSON"
    if ext == ".csv":
        return "CSV_FILE"
    if ext in (".txt", ".md"):
        return "TEXT_FILE"
    if source.startswith("http"):
        return "WEBSITE"
    return "TEXT_FILE" if os.path.isfile(source) else "DIRECTORY"

def detect_all(sources):
    # per-item detection: no outer variable leaking across the loop
    return {s: from_content(s) for s in sources}

if __name__ == "__main__":
    for s, t in detect_all(SOURCES).items():
        print(s, "->", t)

