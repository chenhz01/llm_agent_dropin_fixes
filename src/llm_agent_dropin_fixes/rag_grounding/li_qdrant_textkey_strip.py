# li_qdrant_textkey_strip.py
# Source issue: https://github.com/run-llama/llama_index/issues/23264
# Upstream repo: run-llama/llama_index #23264
# Category: rag_grounding
# Root cause / claim: 从 node.metadata 剥离 text_key，避免非 LlamaIndex 集合的 chunk 被重复送入 LLM。
# Verifier note: self-test：strip 后 metadata 无 page_content，LLM 内容仅出现一次，对应 #23264。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_qdrant_textkey_strip.py
# Fixes run-llama/llama_index#23264: text_key leaked into node.metadata (double-sent to LLM).
# Companion to the Weaviate fix in #22540; usable as a post-load cleanup.

from llama_index.core.schema import MetadataMode, TextNode

def strip_text_key(node: TextNode, text_key: str = "page_content") -> TextNode:
    """Remove the text field from metadata so MetadataMode.LLM doesn't echo it."""
    node.metadata.pop(text_key, None)
    return node

# --- self-test ---
n = TextNode(text="Paris is the capital of France",
             metadata={"page_content": "Paris is the capital of France", "src": "x"})
strip_text_key(n, "page_content")
print(n.metadata.get("page_content"))            # None -> not double-sent
print(n.get_content(MetadataMode.LLM))           # content appears once
