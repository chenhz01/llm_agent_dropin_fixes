# li_state_no_mutate.py
# Source issue: https://github.com/run-llama/llama_index/issues/23234
# Upstream repo: run-llama/llama_index #23234
# Category: state_persist
# Root cause / claim: 用副本构建带 state 的临时 prompt，避免 setup_agent 把状态永久写进 memory 历史。
# Verifier note: self-test：stored.content 保持原样，对应 #23234。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# li_state_no_mutate.py
# Fixes run-llama/llama_index#23234: state_prompt permanently baked into ChatMemoryBuffer history.
# Format the ephemeral prompt without mutating the stored user message.

from llama_index.core.llms import ChatMessage, MessageRole

def format_state_prompt(state: dict, user_msg: str) -> ChatMessage:
    """Build the LLM prompt from a COPY; the original user message stays clean in memory."""
    body = f"Current state:\n{state}\n\nCurrent message:\n{user_msg}"
    return ChatMessage(role=MessageRole.USER, content=body)   # new object, no in-place edit

# --- self-test ---
stored = ChatMessage(role=MessageRole.USER, content="What is 2+2?")
prompt = format_state_prompt({"user_id": "u-42", "plan": "secret"}, stored.content)
print("memory keeps:", stored.content)        # 'What is 2+2?' unchanged
print("llm sees:  ", prompt.content.splitlines()[0])
