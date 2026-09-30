# view_image_bridge.py
# Source issue: https://github.com/labring/FastGPT/issues/7827
# Upstream repo: labring/FastGPT #7827
# Category: ctx_compact
# Root cause / claim: 把工具/沙盒输出的图片 URL 或路径转成 image_url 内容块，补上 #7827 缺失的「图片作为下一轮模型输入」能力。
# Verifier note: py 从工具文本抽取图片 URL/沙盒路径并生成 image_url 块注入下一轮请求，直接对应 issue 复现步骤中 read_files .png 不支持、下一轮无 image_url 的现象。
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

"""view_image_bridge.py - turn a tool/sandbox result into multimodal input for the next model call.
Plug in your own image-store/Sandbox base URL; no keys hardcoded."""

import re

URL_RE = re.compile(r"https?://[^\s]+?\.(?:png|jpe?g|gif|webp|bmp)", re.I)
PATH_RE = re.compile(r"(?:/[^\s]+)+\.(?:png|jpe?g|gif|webp|bmp)", re.I)

def to_image_content(tool_text, sandbox_base=""):
    # sandbox_base: e.g. os.environ["SANDBOX_BASE"] ; prefix for /tmp/*.png paths
    blocks, seen = [], set()
    for url in URL_RE.findall(tool_text):
        if url not in seen:
            blocks.append({"type": "image_url", "image_url": {"url": url}}); seen.add(url)
    for path in PATH_RE.findall(tool_text):
        full = path if not sandbox_base else sandbox_base.rstrip("/") + path
        if full not in seen:
            blocks.append({"type": "image_url", "image_url": {"url": full}}); seen.add(full)
    return blocks

def next_request(messages, tool_text, sandbox_base=""):
    imgs = to_image_content(tool_text, sandbox_base)
    if not imgs:
        return messages  # no pixel data - fall back to text only
    last = messages[-1]
    last["content"] = [{"type": "text", "text": last.get("content", "")}, *imgs]
    return messages

if __name__ == "__main__":
    msgs = [{"role": "user", "content": "describe the screenshot"}]
    out = next_request(msgs, "saved to /tmp/shot.png and https://x/y/z.jpg", "/sbx")
    print(out)

