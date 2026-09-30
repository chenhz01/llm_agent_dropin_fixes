# dify_overlap_splitter.py
# Source issue: https://github.com/langgenius/dify/issues/43000
# Upstream repo: langgenius/dify #43000
# Category: rag_grounding
# Root cause / claim: Character-fallback splitter that holds a constant chunk_overlap on every boundary, fixing the alternating-overlap bug.
# Verifier note: py yields a stable 20-char step and equal 30-char overlaps, fixing the [0,20,51,71,102] alternation in #43000.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Corrected character-fallback splitter that preserves the configured overlap.
# The shipped fallback advances inconsistently, so adjacent overlaps alternate
# (30 then 19) instead of staying at chunk_overlap. Plug in your own text source.

def split_chars(text, chunk_size, chunk_overlap):
    assert 0 <= chunk_overlap < chunk_size
    step = chunk_size - chunk_overlap
    chunks, start = [], 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += step
    return chunks

if __name__ == '__main__':
    text = ''.join(chr(0x4E00 + i) for i in range(130))
    chunks = split_chars(text, chunk_size=50, chunk_overlap=30)
    print([text.index(c) for c in chunks])   # stable 20-char step, 30-char overlap
    print('overlaps:', [len(set(chunks[i]) & set(chunks[i+1])) for i in range(len(chunks)-1)])
