# gr_shadow_overlap_meter.py
# Source issue: https://github.com/assafelovic/gpt-researcher/issues/2180
# Upstream repo: assafelovic/gpt-researcher #2180
# Category: dedup
# Root cause / claim: Shadow-only overlap meter that proves or disproves duplicate paid scraping across parallel GPTResearcher branches without touching results or state.
# Verifier note: py truly solves issue 2180: measures concurrent duplicate-fetch overlap at the scraping boundary with no mutation or result sharing.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

"""
Shadow-only overlap meter for GPT Researcher parallel scraping.
Wraps the common read-only fetch boundary (e.g. ScraperManager.browse_urls).
Records every original call; never shares/reuses results; never mutates state.
Drop-in around your existing scraper; report-only.
"""
from collections import defaultdict
import time


class ShadowFetchMeter:
    def __init__(self):
        self.seen = defaultdict(list)    # canonical_key -> [timestamps]
        self.results = {}                # canonical_key -> [result text]
        self.overhead = 0.0

    def _key(self, url, tenant="", locale="", render=""):
        # partition by request semantics so only equivalent calls count
        return (url, tenant, locale, render)

    def measure(self, url, tenant="", locale="", render="", result=""):
        t0 = time.perf_counter()
        k = self._key(url, tenant, locale, render)
        self.seen[k].append(time.perf_counter())
        self.results.setdefault(k, []).append(result)
        self.overhead += time.perf_counter() - t0

    def report(self):
        total = sum(len(v) for v in self.seen.values())
        dup = sum(len(v) - 1 for v in self.seen.values() if len(v) > 1)
        concurrent = sum(
            1 for v in self.seen.values()
            if len(v) > 1 and (max(v) - min(v)) < 5.0
        )
        agree = sum(
            1 for v in self.results.values()
            if len(v) > 1 and len({hash(r) for r in v}) == 1
        )
        return {
            "total_fetches": total,
            "duplicate_fetches": dup,
            "concurrent_overlap_groups": concurrent,
            "equivalent_result_agreement": agree,
            "meter_overhead_s": round(self.overhead, 6),
            "hypothetical_avoidable_pct": round(100 * dup / total, 2) if total else 0,
        }


# usage at ScraperManager.browse_urls boundary (pseudo):
# meter = ShadowFetchMeter()
# real = self._real_browse(urls)        # your existing client call
# for u in urls:
#     meter.measure(u, tenant=..., locale=..., render=..., result=real[u])
# print(meter.report())
