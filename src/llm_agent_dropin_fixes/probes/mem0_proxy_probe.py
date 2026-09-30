# mem0_proxy_probe.py
# Source issue: https://github.com/mem0ai/mem0/issues/7492
# Upstream repo: mem0ai/mem0 #7492
# Category: other
# Root cause / claim: 突破组件：用 httpx transport 类型探针确认各 provider 是否真的把 http_client_proxies 接通，暴露 17 个 provider 静默丢弃代理的隐患。
# Verifier note: py 针对 issue 7492 直接检测 httpx 传输是否为 HTTPProxy，区分代理接通/直连。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Verify a provider actually routes through your proxy instead of going direct.
# Build the client the way mem0 does, then assert the transport is proxied.
# Plug in your own httpx.Client (e.g. from build_http_client(config)).
import httpx

def proxy_applied(client) -> bool:
    transport = getattr(client, "_transport", None)
    pool = getattr(transport, "_pool", transport)
    return type(pool).__name__ == "HTTPProxy"

if __name__ == "__main__":
    direct = httpx.Client()
    proxied = httpx.Client(proxy="http://127.0.0.1:8080")
    print("direct: ", proxy_applied(direct))    # False -> traffic goes direct
    print("proxied:", proxy_applied(proxied))   # True  -> proxy is wired through
    # False here means the provider's constructor dropped config.http_client.

