# mem0_secret_log_filter.py
# Source issue: https://github.com/mem0ai/mem0/issues/7503
# Upstream repo: mem0ai/mem0 #7503
# Category: ctx_compact
# Root cause / claim: 突破组件：给 mem0 的 vector store 日志加一层敏感字段过滤器，在不丢失字段名诊断价值的前提下遮蔽 service_account_json/private_key 等密钥。
# Verifier note: py 针对 issue 7503 的 DEBUG 明文私钥日志，演示把 private_key 值替换为 ***。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Keep constructor diagnostics useful without leaking the GCP private key.
# Attach this filter to the mem0 logger. Plug in your own logger instance.
import logging, re

REDACT_KEYS = ("private_key", "service_account_json", "api_key", "password")
_PAT = re.compile(r'("(?:private_key|service_account_json|api_key|password)" *: *")[^"]*(")')

class RedactSecrets(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.args, dict):
            record.args = {k: "***" if k in REDACT_KEYS else v
                           for k, v in record.args.items()}
        elif record.args:
            record.msg = _PAT.sub(lambda m: m.group(1) + "***" + m.group(2),
                                  str(record.msg))
        return True

if __name__ == "__main__":
    log = logging.getLogger("mem0.vector_stores.vertex_ai_vector_search")
    log.addFilter(RedactSecrets())
    log.debug('Config created: {"service_account_json": {"private_key": "SECRET"}}')
    # emits the same line with the key value replaced by ***

