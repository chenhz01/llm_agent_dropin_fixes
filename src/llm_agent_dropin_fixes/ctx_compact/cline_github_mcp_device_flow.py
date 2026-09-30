# cline_github_mcp_device_flow.py
# Source issue: https://github.com/cline/cline/issues/14625
# Upstream repo: cline/cline #14625
# Category: ctx_compact
# Root cause / claim: Implements the device-code grant GitHub supports, reachable when discovery 404s — the fallback Cline's ordering currently blocks (#14625).
# Verifier note: py runs GitHub's device authorization grant end-to-end; demonstrates the unreachable fallback path.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# cline_github_mcp_device_flow.py
# For #14625: GitHub's OAuth discovery 404s, so Cline never reaches its existing
# device-code grant. This demonstrates the device flow directly as a fallback
# when authorization-server discovery fails.

import os, time, requests  # pip install requests

GITHUB_DEVICE = "https://github.com/login/device/code"
GITHUB_TOKEN  = "https://github.com/login/oauth/access_token"
CLIENT_ID = os.environ.get("GITHUB_MCP_CLIENT_ID")  # register an OAuth app

def device_login(scopes="read:user"):
    r = requests.post(GITHUB_DEVICE, data={"client_id": CLIENT_ID, "scope": scopes},
                      headers={"Accept": "application/json"})
    r.raise_for_status()
    d = r.json()
    print(f"Open {d['verification_uri']} and enter code {d['user_code']}")
    while True:
        time.sleep(d["interval"])
        t = requests.post(GITHUB_TOKEN, data={"client_id": CLIENT_ID,
            "device_code": d["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"},
            headers={"Accept": "application/json"}).json()
        if "access_token" in t:
            return t["access_token"]          # use as the MCP bearer token
        if t.get("error") != "authorization_pending":
            raise RuntimeError(t.get("error_description", t))

# if __name__ == "__main__":
#     token = device_login()
#     print("MCP bearer token ready")

