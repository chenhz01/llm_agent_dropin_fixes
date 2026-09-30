# mem0_normalize_facts.py
# Source issue: https://github.com/mem0ai/mem0/issues/7446
# Upstream repo: mem0ai/mem0 #7446
# Category: rag_grounding
# Root cause / claim: 突破组件：修正 normalize_facts 对 {'facts':[...]} 整对象与裸字符串的误处理，避免事实抽取结果变成 ['facts'] 或逐字符列表。
# Verifier note: py 针对 issue 7446 的两个失败用例均返回正确字符串列表。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

# Corrected normalize_facts: handles the wrapped {"facts": [...]} object and
# bare strings that the current impl turns into ["facts"] / per-char lists.
# Plug in whatever your LLM fact-extraction step returns.
def normalize_facts(obj) -> list:
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, list):
        out = []
        for it in obj:
            if isinstance(it, str):
                out.append(it)
            elif isinstance(it, dict):
                out.append(it.get("fact") or it.get("text") or "")
            else:
                out.append(str(it))
        return [x for x in out if x]
    if isinstance(obj, dict):
        if "facts" in obj and isinstance(obj["facts"], list):
            return normalize_facts(obj["facts"])
        if "fact" in obj:
            return [obj["fact"]]
    return []

if __name__ == "__main__":
    print(normalize_facts({"facts": ["a", "b"]}))   # ['a', 'b']
    print(normalize_facts("User likes Python"))      # ['User likes Python']

