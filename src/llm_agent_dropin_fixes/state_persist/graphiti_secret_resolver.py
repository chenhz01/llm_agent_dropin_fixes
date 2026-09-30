# graphiti_secret_resolver.py
# Source issue: https://github.com/getzep/graphiti/issues/1887
# Upstream repo: getzep/graphiti #1887
# Category: state_persist
# Root cause / claim: Resolves api_key from a file/callable/env/literal so rotating secrets stay out of env and config.
# Verifier note: py reads _file secret at load and supports dynamic callables.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# graphiti_secret_resolver.py
def resolve_secret(spec):
    """Resolve an api_key spec into the actual secret string.

    spec may be:
      - {"api_key": "<inline-literal>"}              inline literal
      - {"api_key_env": "OPENAI_KEY"}      env var
      - {"api_key_file": "/run/secrets/x"} file (Docker/K8s secret)
      - callable                            dynamic (rotating) value
    """
    if callable(spec):
        return spec()
    if "api_key_file" in spec:
        with open(spec["api_key_file"], encoding="utf-8") as f:
            return f.read().strip()
    if "api_key_env" in spec:
        import os
        return os.environ[spec["api_key_env"]]
    return spec.get("api_key")

# Wire into mcp_server config layer; keep the secret out of env and config.
