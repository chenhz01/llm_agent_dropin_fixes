# cline_models_auth_fetch.py
# Source issue: https://github.com/cline/cline/issues/14685
# Upstream repo: cline/cline #14685
# Category: state_persist
# Root cause / claim: Shows the missing Bearer auth on the model-list fetch that fixes the HTTP 401 in #14685.
# Verifier note: py performs an authenticated GET to /v1/models and parses model ids; mirrors the corrected TS behavior.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# cline_models_auth_fetch.py
# For #14685: fetchModelIdsFromSource omits the API key, so auth-protected
# /v1/models returns 401. This shows the correct call WITH the Authorization
# header that the original TS lacks.

import os, requests  # pip install requests

def fetch_model_ids(base_url, api_key, models_path="/v1/models"):
    # NOTE: plug YOUR gateway URL + key from env; never hardcode a secret.
    url = base_url.rstrip("/") + models_path
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.get(url, headers=headers, timeout=5)
    r.raise_for_status()
    return [m["id"] for m in r.json().get("data", [])]

if __name__ == "__main__":
    key = os.environ.get("CLINE_PROVIDER_KEY")   # your gateway key
    models = fetch_model_ids("http://192.168.99.19:31045", key)
    print("models:", models)

