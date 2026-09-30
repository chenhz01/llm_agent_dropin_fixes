# mem0_openrouter_kwargs.py
# Source issue: https://github.com/mem0ai/mem0/issues/7469
# Upstream repo: mem0ai/mem0 #7469
# Category: ctx_compact
# Root cause / claim: 突破组件：把 OpenRouter 的 models/route 字段正确塞进 extra_body 而非顶层 kwargs，消除每轮 LLM 调用前的 TypeError。
# Verifier note: py 针对 issue 7469 把 models/route 放入 extra_body，避免 OpenAI SDK 报缺少 model 的 TypeError。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Build the kwargs OpenAILLM.generate_response should send for OpenRouter's
# `models` fallback. Plug in your own client + model list.
def openrouter_kwargs(messages, model_list, route="fallback"):
    return {
        "model": model_list[0],
        "messages": messages,
        "extra_body": {"models": model_list, "route": route},
    }

if __name__ == "__main__":
    msgs = [{"role": "user", "content": "I like tea"}]
    models = ["openai/gpt-4o-mini", "anthropic/claude-3.5-haiku"]
    kw = openrouter_kwargs(msgs, models)
    print(kw["model"], "->", kw["extra_body"])
    # client.chat.completions.create(**kw)  # no longer raises TypeError

