# Failure Taxonomy — field guide

Eight recurring failure modes in LLM-agent memory / RAG / context plumbing, each with: **detect → fix shape → representative issues**. Counts reflect the 109 fixes in this library.

## memory_rerank  (`memory_rerank/`)

**Root cause:** 向量相似度 / 重排错乱：距离被当成相似度、缺同义词召回、截断丢记忆。

**Count:** 11 fixes

**How to detect:**

- Nearest-neighbor search returns the wrong item.
- Relevance ranking is inverted or non-monotonic.
- Synonym / paraphrased queries miss obvious matches.

**Fix shape:**

Normalize the score space (distance → monotonic similarity), add synonym/expansion recall, and bound the recall window.

**Representative issues:**

- [getzep/graphiti #1888](https://github.com/getzep/graphiti/issues/1888) — Reranks the full 2*limit candidate set before truncating to limit, so the cross-…
- [getzep/graphiti #1897](https://github.com/getzep/graphiti/issues/1897) — Pairs every returned edge with its source's node-distance score so shared-source…
- [kingjulio8238/Memary #49](https://github.com/kingjulio8238/Memary/issues/49) — Implements the LLMSynonymRetriever concept from issue #49: expands queries into …
- [labring/FastGPT #7113](https://github.com/labring/FastGPT/issues/7113) — 把 RAG 检索→重排→最终上下文做成可观测 trace，直接对应 #7113 的 Retrieval Trace View 诉求（retrieved/rera…
- [langgenius/dify #42996](https://github.com/langgenius/dify/issues/42996) — Detects the vectorizer:none misconfiguration and embeds the query client-side so…
- [langgenius/dify #43062](https://github.com/langgenius/dify/issues/43062) — Audits an imported workflow DSL for knowledge-retrieval nodes whose dataset_ids …
- [mem0ai/mem0 #7482](https://github.com/mem0ai/mem0/issues/7482) — 将 Pinecone 欧氏索引返回的 squared-distance 还原成单调递增相似度并重排，修复 Memory.search 在 L2 索引上丢最近记忆…
- [run-llama/llama_index #23199](https://github.com/run-llama/llama_index/issues/23199) — 在邻居扩展后保留原始检索分数，防止 PrevNextNodePostprocessor 把已知分数覆盖成 None。
- … and 3 more in `src/llm_agent_dropin_fixes/memory_rerank/`

## state_persist  (`state_persist/`)

**Root cause:** 状态 / 历史持久化错乱：跨时区排序颠倒、凭据审计被静默抹除、孤儿记录堆积。

**Count:** 31 fixes

**How to detect:**

- Audit/history logs order events incorrectly across timezones.
- Credential/config fields silently blanked on clone.
- Orphan records accumulate and bloat storage.

**Fix shape:**

Sort by timezone-aware instants, audit sensitive fields before clone, and reap orphans with a bounded sweep.

**Representative issues:**

- [cline/cline #14622](https://github.com/cline/cline/issues/14622) — Lists orphaned MCP server processes that outlive their session, giving the hub a…
- [cline/cline #14642](https://github.com/cline/cline/issues/14642) — Flags sessions whose updatedAt resets to 'now' on launch without new activity, p…
- [cline/cline #14682](https://github.com/cline/cline/issues/14682) — Prunes deleted folders from the persisted workspace list so the switcher stops s…
- [cline/cline #14685](https://github.com/cline/cline/issues/14685) — Shows the missing Bearer auth on the model-list fetch that fixes the HTTP 401 in…
- [cline/cline #14699](https://github.com/cline/cline/issues/14699) — Audits which settings scope grants a permission, surfacing the project-vs-user a…
- [cline/cline #14700](https://github.com/cline/cline/issues/14700) — Detects orphaned remote-helper daemons re-parented to init, giving the hub a con…
- [crewAIInc/crewAI #7746](https://github.com/crewAIInc/crewAI/issues/7746) — Storage shim that serializes any JSON-able value on update and tolerates NULL on…
- [crewAIInc/crewAI #7775](https://github.com/crewAIInc/crewAI/issues/7775) — Cache-tagged tool wrapper that emits ToolUsageFinishedEvent(from_cache=True) on …
- … and 23 more in `src/llm_agent_dropin_fixes/state_persist/`

## ctx_compact  (`ctx_compact/`)

**Root cause:** 上下文压缩 / 客户端适配错乱：OpenRouter kwargs 误传、Langchain 兜底、嵌套属性序列化。

**Count:** 14 fixes

**How to detect:**

- Compaction drops or mangles messages.
- Provider-specific kwargs (e.g. OpenRouter) misrouted.
- Nested/non-serializable attributes crash serialization.

**Fix shape:**

Route provider kwargs correctly, add a safe list/refine fallback, and serialize nested attrs deterministically.

**Representative issues:**

- [cline/cline #14625](https://github.com/cline/cline/issues/14625) — Implements the device-code grant GitHub supports, reachable when discovery 404s …
- [cline/cline #14694](https://github.com/cline/cline/issues/14694) — Trims/summarizes oldest turns to a token budget so large-context sessions don't …
- [crewAIInc/crewAI #7766](https://github.com/crewAIInc/crewAI/issues/7766) — Targeted shim that swaps the hard-coded 'you MUST return...' line for the softer…
- [getzep/graphiti #1869](https://github.com/getzep/graphiti/issues/1869) — Consults the model's real output budget for extract_edges instead of the hard-co…
- [getzep/graphiti #1885](https://github.com/getzep/graphiti/issues/1885) — Serializes legitimately nested attributes to JSON strings for all providers and …
- [kingjulio8238/Memary #42](https://github.com/kingjulio8238/Memary/issues/42) — Filters Memary's top-N entities down to those literally/near-present in the agen…
- [labring/FastGPT #7827](https://github.com/labring/FastGPT/issues/7827) — 把工具/沙盒输出的图片 URL 或路径转成 image_url 内容块，补上 #7827 缺失的「图片作为下一轮模型输入」能力。
- [langchain-ai/langchain #40840](https://github.com/langchain-ai/langchain/issues/40840) — Recognizes Bedrock Claude token counts so SummarizationMiddleware compacts conte…
- … and 6 more in `src/llm_agent_dropin_fixes/ctx_compact/`

## rag_grounding  (`rag_grounding/`)

**Root cause:** RAG 检索过滤错乱：Pinecone/Qdrant 过滤语法被包错、空 PDF 静默、重叠切片。

**Count:** 8 fixes

**How to detect:**

- Vector search returns HTTP 400 on $or/$not filters.
- Empty/garbled PDFs ingested silently with no signal.
- Overlapping text chunks double-count context.

**Fix shape:**

Translate filters into native vector-DB syntax, fail loud on empty extractions, and de-overlap chunks.

**Representative issues:**

- [crewAIInc/crewAI #7827](https://github.com/crewAIInc/crewAI/issues/7827) — Per-item, case-normalized data_type detection that kills the outer-variable leak…
- [getzep/graphiti #1880](https://github.com/getzep/graphiti/issues/1880) — Grounds extracted edges in source text via lexical overlap, flagging misattribut…
- [langgenius/dify #43000](https://github.com/langgenius/dify/issues/43000) — Character-fallback splitter that holds a constant chunk_overlap on every boundar…
- [mem0ai/mem0 #7443](https://github.com/mem0ai/mem0/issues/7443) — 把 pgvector 过滤值里的 Python 布尔归一为小写 JSON 文本，修复 eq/ne/in/nin 布尔过滤永不命中（及 ne/nin 静默返回被排…
- [mem0ai/mem0 #7446](https://github.com/mem0ai/mem0/issues/7446) — 修正 normalize_facts 对 {'facts':[...]} 整对象与裸字符串的误处理，避免事实抽取结果变成 ['facts'] 或逐字符列表。
- [mem0ai/mem0 #7468](https://github.com/mem0ai/mem0/issues/7468) — 把合并在同一字段上的多个操作符拆成独立 AND 条件，修复 Qdrant 只应用首个操作符导致被排除记忆被返回的 bug。
- [mem0ai/mem0 #7483](https://github.com/mem0ai/mem0/issues/7483) — 把 mem0 的 $or/$not 与 eq/in/ne 操作符正确翻译成 Pinecone 原生过滤语法，消除每类 OR/NOT 搜索的 HTTP 400。
- [run-llama/llama_index #23264](https://github.com/run-llama/llama_index/issues/23264) — 从 node.metadata 剥离 text_key，避免非 LlamaIndex 集合的 chunk 被重复送入 LLM。

## loop_guard  (`loop_guard/`)

**Root cause:** 外部调用 / 生成循环失控：静默挂死、重复循环、缺超时重试与日志。

**Count:** 7 fixes

**How to detect:**

- A run hangs forever with no logs.
- The same step repeats without progress.
- No timeout/retry around external calls.

**Fix shape:**

Wrap external calls in a bounded guard (hard timeout + retry + logging); add a max-iteration breaker.

**Representative issues:**

- [assafelovic/gpt-researcher #1764](https://github.com/assafelovic/gpt-researcher/issues/1764) — Thread-based bounded-call guard that turns silent external-call hangs into logge…
- [cline/cline #14702](https://github.com/cline/cline/issues/14702) — Isolates each user turn behind a stop token so a follow-up cannot resume a cance…
- [crewAIInc/crewAI #7757](https://github.com/crewAIInc/crewAI/issues/7757) — Constructor guard that rejects max_iter < 1, turning the nonsense RecursionError…
- [crewAIInc/crewAI #7758](https://github.com/crewAIInc/crewAI/issues/7758) — Static validator that fails fast when a Flow has no @start() entrypoint, prevent…
- [getzep/graphiti #1922](https://github.com/getzep/graphiti/issues/1922) — Detects extract_edges repetition loops and re-rolls at higher temperature instea…
- [labring/FastGPT #7665](https://github.com/labring/FastGPT/issues/7665) — 在工具执行期插入协作式停止检查与迭代上限，消除 #7665 指出的 base.ts:532 await 期间不检查停止信号的竞态。
- [run-llama/llama_index #23298](https://github.com/run-llama/llama_index/issues/23298) — 用 asyncio.to_thread 把同步 query 卸到线程，避免 aquery 阻塞事件循环。

## dedup  (`dedup/`)

**Root cause:** 去重非确定性 / 重复抓取：tiebreak 不稳、shadow 重叠重复计。

**Count:** 4 fixes

**How to detect:**

- Same entity inserted multiple times.
- Tiebreak is non-deterministic across runs.
- Shadow/overlap windows double-count.

**Fix shape:**

Add a deterministic tiebreak key and a shadow/overlap meter to catch double insertion.

**Representative issues:**

- [assafelovic/gpt-researcher #2180](https://github.com/assafelovic/gpt-researcher/issues/2180) — Shadow-only overlap meter that proves or disproves duplicate paid scraping acros…
- [crewAIInc/crewAI #7783](https://github.com/crewAIInc/crewAI/issues/7783) — Event-bus probe that counts LLMCallFailedEvent so the double-emission / scope-po…
- [getzep/graphiti #1872](https://github.com/getzep/graphiti/issues/1872) — Merges identical facts across a bulk batch into one edge with combined episode u…
- [getzep/graphiti #1916](https://github.com/getzep/graphiti/issues/1916) — Breaks fuzzy-dedup ties on candidate uuid (sorted) so resolution is deterministi…

## token_guard  (`token_guard/`)

**Root cause:** token 计费 / 限流护栏：计数漏算、桶死锁、限流器形同虚设。

**Count:** 3 fixes

**How to detect:**

- Billed tokens diverge from actual usage.
- Rate limiter never blocks (or deadlocks).
- Token buckets freeze under load.

**Fix shape:**

Count tokens at the real boundary, make the limiter actually gate, and avoid bucket deadlocks.

**Representative issues:**

- [run-llama/llama_index #23202](https://github.com/run-llama/llama_index/issues/23202) — 对超出桶容量的请求快速失败而非死锁，修复 TokenBucket 永久阻塞与 SlidingWindow 放行超限。
- [run-llama/llama_index #23267](https://github.com/run-llama/llama_index/issues/23267) — 检测 prompt 中重复出现的 format 块，作为回归守卫捕捉多选提示被重复注入。
- [run-llama/llama_index #23313](https://github.com/run-llama/llama_index/issues/23313) — 对 tool_calls 同时兼容 dict 形态并对 None 名称/参数做护栏，消除 TokenCounter 漏算与 TypeError。

## other  (`probes/`)

**Root cause:** 静默失效探针：代理路由、凭据、PDF 空提取等看不见的退化哨兵。

**Count:** 31 fixes

**How to detect:**

- Silent degradations with no error surfaced.
- Proxy/credential routes quietly fail.
- Empty extractions pass as success.

**Fix shape:**

Add a probe that fails loud instead of silent, surfacing the degraded path with a clear signal.

**Representative issues:**

- [assafelovic/gpt-researcher #1582](https://github.com/assafelovic/gpt-researcher/issues/1582) — Silent-empty PDF extraction probe that catches scanned/image-only PDFs where the…
- [cline/cline #14649](https://github.com/cline/cline/issues/14649) — Guards the reasoning level against each model's supported enum, preventing the U…
- [crewAIInc/crewAI #7764](https://github.com/crewAIInc/crewAI/issues/7764) — Factory that gives LLMGuardrail its own judge LLM, falling back to the agent's —…
- [crewAIInc/crewAI #7789](https://github.com/crewAIInc/crewAI/issues/7789) — Local in-memory PII sanitizer with deterministic surrogates + length-ordered res…
- [getzep/graphiti #1874](https://github.com/getzep/graphiti/issues/1874) — Selects the OpenAI client from an explicit api_mode instead of hostname inferenc…
- [getzep/graphiti #1909](https://github.com/getzep/graphiti/issues/1909) — Forces all json_schema properties required so grammar backends emit valid_at/inv…
- [getzep/graphiti #1919](https://github.com/getzep/graphiti/issues/1919) — Expands '*' to all groups and reports the searched scope so empty results aren't…
- [getzep/graphiti #1931](https://github.com/getzep/graphiti/issues/1931) — Diffs add_episode prompt output across PYTHONHASHSEED values to catch non-determ…
- … and 23 more in `src/llm_agent_dropin_fixes/probes/`

