# gr_pdf_silent_empty_probe.py
# Source issue: https://github.com/assafelovic/gpt-researcher/issues/1582
# Upstream repo: assafelovic/gpt-researcher #1582
# Category: other
# Root cause / claim: Silent-empty PDF extraction probe that catches scanned/image-only PDFs where the MIT pdfminer.six scraper yields empty context, pinpointing where an OCR fallback is needed.
# Verifier note: py addresses issue 1582's operational gap: flags silent-empty pdfminer extractions; the license decision itself is the maintainer's.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

"""
PDF extraction sanity probe for the MIT (pdfminer.six) scraper.
pdfminer.six returns EMPTY text on scanned / image-only PDFs — silently.
This flags those cases so your MIT scraper doesn't feed empty context
and tells you where an OCR fallback is actually needed.
"""
import os
import sys

# PLUG IN YOUR OWN SCRAPER HERE (the PDFMinerScraper from this issue):
# from your_scraper import PDFMinerScraper

MIN_CHARS = 200   # below this we treat extraction as effectively empty


def probe(pdf_path):
    # content, _, title = PDFMinerScraper(pdf_path).scrape()
    from pdfminer.high_level import extract_text
    try:
        text = extract_text(pdf_path) or ""
    except Exception as e:
        return {"file": pdf_path, "status": "error", "detail": str(e)}
    if len(text.strip()) < MIN_CHARS:
        return {"file": pdf_path, "status": "EMPTY_SILENT",
                "chars": len(text), "needs_ocr": True}
    return {"file": pdf_path, "status": "ok", "chars": len(text)}


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith(".pdf"):
                print(probe(os.path.join(dirpath, f)))
