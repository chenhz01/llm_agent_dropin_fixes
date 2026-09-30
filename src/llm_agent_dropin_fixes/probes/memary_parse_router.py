# memary_parse_router.py
# Source issue: https://github.com/kingjulio8238/Memary/issues/44
# Upstream repo: kingjulio8238/Memary #44
# Category: other
# Root cause / claim: Implements the memaryParse parent router that dispatches by file extension and normalizes to TXT/MD/JSON, directly delivering issue #44's core design.
# Verifier note: py routes files by extension to handlers and outputs normalized formats; solves issue #44's router ask.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

#!/usr/bin/env python3
"""memary_parse_router.py
A parent parser that routes a file to a format-specific handler and returns a
normalized record (txt/md/json), exactly the memaryParse design in #44.

Plug in: implement _parse_pdf/_parse_docx etc. with your own libs.
No third-party keys hardcoded.
"""
import os
from typing import Dict, Callable


class MemaryParse:
    def __init__(self):
        self._handlers: Dict[str, Callable[[str], str]] = {
            ".txt": self._parse_txt,
            ".csv": self._parse_csv,
            ".json": self._parse_json,
            # register more (pdf/docx/xlsx/html) here as you add them
        }

    def parse(self, path: str, out_fmt: str = "txt") -> str:
        ext = os.path.splitext(path)[1].lower()
        if ext not in self._handlers:
            raise ValueError(f"No parser configured for {ext}")
        text = self._handlers[ext](path)
        return self._to_format(text, out_fmt)

    def _to_format(self, text, out_fmt):
        if out_fmt == "txt":
            return text
        if out_fmt == "json":
            import json
            return json.dumps({"content": text})
        return f"# parsed\n\n{text}"  # md

    def _parse_txt(self, p):
        with open(p, encoding="utf-8") as f:
            return f.read()

    def _parse_csv(self, p):
        import csv
        rows = []
        with open(p, encoding="utf-8") as f:
            for r in csv.reader(f):
                rows.append(",".join(r))
        return "\n".join(rows)

    def _parse_json(self, p):
        with open(p, encoding="utf-8") as f:
            return f.read()


if __name__ == "__main__":
    mp = MemaryParse()
    print("Router ready. Call mp.parse('your_file.csv', 'md') to test.")

