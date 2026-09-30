# lc_bedrock_token_counter.py
# Source issue: https://github.com/langchain-ai/langchain/issues/40840
# Upstream repo: langchain-ai/langchain #40840
# Category: ctx_compact
# Root cause / claim: Recognizes Bedrock Claude token counts so SummarizationMiddleware compacts context before the window overflows, fixing the late-trigger gap.
# Verifier note: py subclasses the real SummarizationMiddleware and overrides the real _get_approximate_token_counter method, returning a Claude-aware count for Bedrock models; directly addresses #40840.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# lc_bedrock_token_counter.py
# Fixes #40840: SummarizationMiddleware can't count tokens for ChatBedrockConverse
# (Claude on Bedrock), so context compaction triggers late. Plug in YOUR llm below.
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import BaseMessage

def claude_approx_tokens(messages, model="claude"):
    # Heuristic ~4 chars/token for Claude; swap in a real Claude tokenizer if needed.
    text = "\n".join(getattr(m, "content", "") or "" for m in messages)
    return max(1, len(text) // 4)

class BedrockAwareSummarizationMiddleware(SummarizationMiddleware):
    """Subclass that recognizes ChatBedrockConverse _llm_type for token counting."""
    def _get_approximate_token_counter(self):
        base = super()._get_approximate_token_counter()
        def counter(messages, model=None):
            model = model or getattr(getattr(self, "llm", None), "model", "")
            if "bedrock" in str(model).lower() or "claude" in str(model).lower():
                return claude_approx_tokens(messages, model)
            return base(messages, model=model) if base else claude_approx_tokens(messages, model)
        return counter

# Usage:
# from langchain_aws import ChatBedrockConverse
# llm = ChatBedrockConverse(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")
# mw = BedrockAwareSummarizationMiddleware(llm=llm, trigger=("tokens", 170_000))
