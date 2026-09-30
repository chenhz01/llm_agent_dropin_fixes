# cognee_workflow_lint.py
# Source issue: https://github.com/topoteretes/cognee/issues/4865
# Upstream repo: topoteretes/cognee #4865
# Category: other
# Root cause / claim: 本地扫描缺扩展名的工作流文件并校验 PR 标题语义类型，先把 #4865 的 pr_lint 改名 + 开启前自检。
# Verifier note: py 针对 issue 所述 pr_lint 无扩展名不被加载 + 标题类型校验，可运行。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

import os, re, sys

# Local guard for the CI gap in #4865: flag extensionless workflow files and
# validate PR titles against the semantic type list before re-enabling.
# Plug in: run in pre-commit or a one-off check.

WORKFLOWS_DIR = ".github/workflows"
TYPE_LIST = ("feat", "fix", "docs", "style", "refactor", "perf",
             "test", "build", "ci", "chore", "revert")
TITLE_RE = re.compile(r"^(" + "|".join(TYPE_LIST) + r")(\(.+\))?!?: .+")

def find_extensionless():
    bad = []
    for f in os.listdir(WORKFLOWS_DIR):
        if not re.search(r"\.(ya?ml)$", f):
            bad.append(f)   # e.g. 'pr_lint' -> rename to pr_lint.yml
    return bad

def validate_title(title):
    return bool(TITLE_RE.match(title.strip()))

if __name__ == "__main__":
    bad = find_extensionless()
    if bad:
        print("extensionless workflows (rename to .yml):", bad)
    title = sys.argv[1] if len(sys.argv) > 1 else "fix: rename pr_lint workflow"
    print("title ok:", validate_title(title))

