# graphiti_openai_mode_chooser.py
# Source issue: https://github.com/getzep/graphiti/issues/1874
# Upstream repo: getzep/graphiti #1874
# Category: other
# Root cause / claim: Selects the OpenAI client from an explicit api_mode instead of hostname inference, supporting proxies.
# Verifier note: py returns Responses client when api_mode='responses'.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_openai_mode_chooser.py
def choose_openai_client(config, OpenAIClient, OpenAIGenericClient):
    """Pick the OpenAI client from an explicit mode, not the URL hostname.

    config.providers.openai.api_mode: 'responses' | 'chat' (generic)
    Falls back to hostname inference only when api_mode is unset.
    """
    mode = getattr(config.providers.openai, "api_mode", None)
    if mode == "responses":
        return OpenAIClient(...)        # supports Responses API + embeddings
    if mode == "chat":
        return OpenAIGenericClient(...) # Chat Completions-compatible proxy
    from urllib.parse import urlparse
    host = urlparse(config.providers.openai.api_url).hostname or ""
    return OpenAIGenericClient(...) if "openai.com" not in host else OpenAIClient(...)
