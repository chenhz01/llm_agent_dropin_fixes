# llm_agent_dropin_fixes

Drop-in, **tested** reference fixes for recurring LLM-agent memory / RAG / context bugs — mined from 100+ real upstream issues across mem0, Langchain, Graphiti, Cline, Dify, GPT-Researcher and more.

> **Published** at [`chenhz01/llm_agent_dropin_fixes`](https://github.com/chenhz01/llm_agent_dropin_fixes). Each fix is an independent reference implementation derived from a public issue — **not affiliated with, endorsed by, or copied from** the upstream projects. Plug in your own client/model; no hardcoded keys.

## Why this exists

The same classes of bugs keep surfacing in LLM-agent stacks: a vector distance silently treated as a similarity score, a history log sorted by string instead of real time, an external call that hangs with no timeout. This library collects **109 minimal, dependency-light reference fixes**, each annotated with the source issue, the upstream repo, the root-cause claim, and a verifier note. Use them as drop-in patches or as a checklist when auditing your own agent.

## Install (local, editable)

```bash
cd llm_agent_dropin_fixes
pip install -e .        # or: pip install .
```

## Dependencies

**Zero install-time dependencies.** `pip install llm_agent_dropin_fixes` pulls in
nothing but the package itself, and `import llm_agent_dropin_fixes` never eagerly
imports any third-party library — so the package can't break your environment.

A handful of individual fixes are written *against* a specific library
(`langchain`, `llama_index`, `crewai`, `httpx`, `pdfminer`, …) and `import` that
library at the top of the module. Those imports are **lazy and scoped to that one
fix** — they only fire when you actually use that module, and you supply the
client. If you don't use that fix, the library is never imported. Every fix is
self-contained source you read, adapt, and paste; nothing is a hidden
requirement.

## Quickstart — plug-in pattern

Every fix is a small, self-contained function. You supply your own client/model; nothing is hardcoded.

```python
from llm_agent_dropin_fixes.state_persist.mem0_history_resort import resort_history

# mem0 history() returns events keyed by created_at as strings.
# String sort breaks across timezones; re-sort by real instant:
events = [
    {"created_at": "2026-01-01T09:00:00+00:00", "event": "UPDATE"},
    {"created_at": "2026-01-01T10:00:00+08:00", "event": "ADD"},
]
ordered = resort_history(events)   # ADD (01:00 UTC) now precedes UPDATE (09:00 UTC)
```

## Failure taxonomy (8 classes)

| Class | Subpackage | Root cause | Fixes |
|-------|-----------|-----------|-------|
| memory_rerank | `memory_rerank` | 向量相似度 / 重排错乱：距离被当成相似度、缺同义词召回、截断丢记忆。 | 11 |
| state_persist | `state_persist` | 状态 / 历史持久化错乱：跨时区排序颠倒、凭据审计被静默抹除、孤儿记录堆积。 | 31 |
| ctx_compact | `ctx_compact` | 上下文压缩 / 客户端适配错乱：OpenRouter kwargs 误传、Langchain 兜底、嵌套属性序列化。 | 14 |
| rag_grounding | `rag_grounding` | RAG 检索过滤错乱：Pinecone/Qdrant 过滤语法被包错、空 PDF 静默、重叠切片。 | 8 |
| loop_guard | `loop_guard` | 外部调用 / 生成循环失控：静默挂死、重复循环、缺超时重试与日志。 | 7 |
| dedup | `dedup` | 去重非确定性 / 重复抓取：tiebreak 不稳、shadow 重叠重复计。 | 4 |
| token_guard | `token_guard` | token 计费 / 限流护栏：计数漏算、桶死锁、限流器形同虚设。 | 3 |
| other | `probes` | 静默失效探针：代理路由、凭据、PDF 空提取等看不见的退化哨兵。 | 31 |

See [`docs/FAILURE_TAXONOMY.md`](docs/FAILURE_TAXONOMY.md) for the full field guide (detect → fix shape → representative issues).

## Full index (by class)

### memory_rerank  (`memory_rerank/`) — 11 fixes

> 向量相似度 / 重排错乱：距离被当成相似度、缺同义词召回、截断丢记忆。

- [`memory_rerank/graphiti_episode_search_rerank.py`](src/llm_agent_dropin_fixes/memory_rerank/graphiti_episode_search_rerank.py) — [getzep/graphiti #1888](https://github.com/getzep/graphiti/issues/1888) — Reranks the full 2*limit candidate set before truncating to limit, so the cross-encoder sees all candidates.
- [`memory_rerank/graphiti_node_distance_align.py`](src/llm_agent_dropin_fixes/memory_rerank/graphiti_node_distance_align.py) — [getzep/graphiti #1897](https://github.com/getzep/graphiti/issues/1897) — Pairs every returned edge with its source's node-distance score so shared-source facts aren't misaligned.
- [`memory_rerank/memary_synonym_retriever.py`](src/llm_agent_dropin_fixes/memory_rerank/memary_synonym_retriever.py) — [kingjulio8238/Memary #49](https://github.com/kingjulio8238/Memary/issues/49) — Implements the LLMSynonymRetriever concept from issue #49: expands queries into synonyms then de-dupes retrieval hits to surface more relevant graph nodes.
- [`memory_rerank/retrieval_trace.py`](src/llm_agent_dropin_fixes/memory_rerank/retrieval_trace.py) — [labring/FastGPT #7113](https://github.com/labring/FastGPT/issues/7113) — 把 RAG 检索→重排→最终上下文做成可观测 trace，直接对应 #7113 的 Retrieval Trace View 诉求（retrieved/reranked/final_context/source attribution 四段）。
- [`memory_rerank/dify_hybrid_diagnostic.py`](src/llm_agent_dropin_fixes/memory_rerank/dify_hybrid_diagnostic.py) — [langgenius/dify #42996](https://github.com/langgenius/dify/issues/42996) — Detects the vectorizer:none misconfiguration and embeds the query client-side so hybrid retrieval returns chunks even before the rebuild.
- [`memory_rerank/dify_dsl_dataset_audit.py`](src/llm_agent_dropin_fixes/memory_rerank/dify_dsl_dataset_audit.py) — [langgenius/dify #43062](https://github.com/langgenius/dify/issues/43062) — Audits an imported workflow DSL for knowledge-retrieval nodes whose dataset_ids can't decrypt, converting a silent drop into a visible warning.
- [`memory_rerank/mem0_pinecone_l2_rescore.py`](src/llm_agent_dropin_fixes/memory_rerank/mem0_pinecone_l2_rescore.py) — [mem0ai/mem0 #7482](https://github.com/mem0ai/mem0/issues/7482) — 突破组件：将 Pinecone 欧氏索引返回的 squared-distance 还原成单调递增相似度并重排，修复 Memory.search 在 L2 索引上丢最近记忆的问题。
- [`memory_rerank/li_prevnext_score_fix.py`](src/llm_agent_dropin_fixes/memory_rerank/li_prevnext_score_fix.py) — [run-llama/llama_index #23199](https://github.com/run-llama/llama_index/issues/23199) — 在邻居扩展后保留原始检索分数，防止 PrevNextNodePostprocessor 把已知分数覆盖成 None。
- [`memory_rerank/li_choice_select_fix.py`](src/llm_agent_dropin_fixes/memory_rerank/li_choice_select_fix.py) — [run-llama/llama_index #23273](https://github.com/run-llama/llama_index/issues/23273) — 将 choice-select 解析收紧到 1..num_choices 的 1-based 边界，杜绝 0/负数静默指向末节点。
- [`memory_rerank/cognee_triplet_backfill.py`](src/llm_agent_dropin_fixes/memory_rerank/cognee_triplet_backfill.py) — [topoteretes/cognee #4822](https://github.com/topoteretes/cognee/issues/4822) — 从端点节点的 node_map 回填 belongs_to_set 到 Triplet/EdgeType 载荷，修复 node-set 过滤 triplet 检索恒为空 + 全表扫描。
- [`memory_rerank/cognee_recall_cutoff.py`](src/llm_agent_dropin_fixes/memory_rerank/cognee_recall_cutoff.py) — [topoteretes/cognee #5222](https://github.com/topoteretes/cognee/issues/5222) — 对 recall 结果做融合分阈值截断 + 标识符型词法 boost，让噪声 prompt 返回空、commit SHA/工单号精确命中回到前列。

### state_persist  (`state_persist/`) — 31 fixes

> 状态 / 历史持久化错乱：跨时区排序颠倒、凭据审计被静默抹除、孤儿记录堆积。

- [`state_persist/cline_mcp_orphan_reaper.py`](src/llm_agent_dropin_fixes/state_persist/cline_mcp_orphan_reaper.py) — [cline/cline #14622](https://github.com/cline/cline/issues/14622) — Lists orphaned MCP server processes that outlive their session, giving the hub a reaper hook for /clear and quit (#14622).
- [`state_persist/cline_session_time_auditor.py`](src/llm_agent_dropin_fixes/state_persist/cline_session_time_auditor.py) — [cline/cline #14642](https://github.com/cline/cline/issues/14642) — Flags sessions whose updatedAt resets to 'now' on launch without new activity, pinpointing the phantom-timestamp bug (#14642).
- [`state_persist/cline_workspace_pruner.py`](src/llm_agent_dropin_fixes/state_persist/cline_workspace_pruner.py) — [cline/cline #14682](https://github.com/cline/cline/issues/14682) — Prunes deleted folders from the persisted workspace list so the switcher stops showing dead entries (#14682).
- [`state_persist/cline_models_auth_fetch.py`](src/llm_agent_dropin_fixes/state_persist/cline_models_auth_fetch.py) — [cline/cline #14685](https://github.com/cline/cline/issues/14685) — Shows the missing Bearer auth on the model-list fetch that fixes the HTTP 401 in #14685.
- [`state_persist/cline_perm_scope_auditor.py`](src/llm_agent_dropin_fixes/state_persist/cline_perm_scope_auditor.py) — [cline/cline #14699](https://github.com/cline/cline/issues/14699) — Audits which settings scope grants a permission, surfacing the project-vs-user allow discrepancy behind the silent refusals in #14699.
- [`state_persist/cline_orphan_daemon_reaper.py`](src/llm_agent_dropin_fixes/state_persist/cline_orphan_daemon_reaper.py) — [cline/cline #14700](https://github.com/cline/cline/issues/14700) — Detects orphaned remote-helper daemons re-parented to init, giving the hub a concrete reaper hook for the leak/OOM in #14700.
- [`state_persist/kickoff_storage_shim.py`](src/llm_agent_dropin_fixes/state_persist/kickoff_storage_shim.py) — [crewAIInc/crewAI #7746](https://github.com/crewAIInc/crewAI/issues/7746) — Storage shim that serializes any JSON-able value on update and tolerates NULL on load, fixing the crash in KickoffTaskOutputsSQLiteStorage.
- [`state_persist/from_cache_probe.py`](src/llm_agent_dropin_fixes/state_persist/from_cache_probe.py) — [crewAIInc/crewAI #7775](https://github.com/crewAIInc/crewAI/issues/7775) — Cache-tagged tool wrapper that emits ToolUsageFinishedEvent(from_cache=True) on replays, fixing the silent provenance bug.
- [`state_persist/sqlite_wal_retry.py`](src/llm_agent_dropin_fixes/state_persist/sqlite_wal_retry.py) — [crewAIInc/crewAI #7822](https://github.com/crewAIInc/crewAI/issues/7822) — Bounded exponential-backoff wrapper around PRAGMA journal_mode=WAL that removes the 'database is locked' race the maintainer's PR #7821 targets.
- [`state_persist/graphiti_temporal_overlap.py`](src/llm_agent_dropin_fixes/state_persist/graphiti_temporal_overlap.py) — [getzep/graphiti #1865](https://github.com/getzep/graphiti/issues/1865) — Checks validity-interval overlap before reusing a historical edge, preserving disjoint occurrences.
- [`state_persist/graphiti_read_scope_resolver.py`](src/llm_agent_dropin_fixes/state_persist/graphiti_read_scope_resolver.py) — [getzep/graphiti #1876](https://github.com/getzep/graphiti/issues/1876) — Derives the read driver from group_id like _resolve_request_scope, so reads follow the write's database.
- [`state_persist/graphiti_secret_resolver.py`](src/llm_agent_dropin_fixes/state_persist/graphiti_secret_resolver.py) — [getzep/graphiti #1887](https://github.com/getzep/graphiti/issues/1887) — Resolves api_key from a file/callable/env/literal so rotating secrets stay out of env and config.
- [`state_persist/graphiti_queue_retry.py`](src/llm_agent_dropin_fixes/state_persist/graphiti_queue_retry.py) — [getzep/graphiti #1911](https://github.com/getzep/graphiti/issues/1911) — Retries transient ingest errors with backoff+jitter and re-queues episodes left with 0 edges.
- [`state_persist/egress_policy.py`](src/llm_agent_dropin_fixes/state_persist/egress_policy.py) — [labring/FastGPT #7345](https://github.com/labring/FastGPT/issues/7345) — 用通配符域名匹配实现 allow/deny 出网策略（默认 deny=fail-closed）并做命中词脱敏，对应 #7345 的 1.5 通配符与 3.2 redact。
- [`state_persist/x402_detect.py`](src/llm_agent_dropin_fixes/state_persist/x402_detect.py) — [labring/FastGPT #7837](https://github.com/labring/FastGPT/issues/7837) — 结构化识别 MCP 工具返回的 payment_required/payment_challenge，而非原样透传为文本，对应 #7837 的 detect it structurally 诉求。
- [`state_persist/train_queue_checkpoint.py`](src/llm_agent_dropin_fixes/state_persist/train_queue_checkpoint.py) — [labring/FastGPT #7879](https://github.com/labring/FastGPT/issues/7879) — 把训练队列做成可暂停的 checkpoint 状态机，暂停时持久化已完成分块、恢复后从剩余继续，对应 #7879 的文档级/全局暂停与停止删除解耦。
- [`state_persist/lc_fallback_input_guard.py`](src/llm_agent_dropin_fixes/state_persist/lc_fallback_input_guard.py) — [langchain-ai/langchain #40878](https://github.com/langchain-ai/langchain/issues/40878) — Prevents with_fallbacks from corrupting the caller's input state by deep-copying before the fallback path runs.
- [`state_persist/dify_vars_paginator.py`](src/llm_agent_dropin_fixes/state_persist/dify_vars_paginator.py) — [langgenius/dify #43084](https://github.com/langgenius/dify/issues/43084) — Keyset pagination on (created_at, id) makes conversation-variable ordering deterministic so tied timestamps never skip a variable.
- [`state_persist/dify_logs_paginator.py`](src/llm_agent_dropin_fixes/state_persist/dify_logs_paginator.py) — [langgenius/dify #43134](https://github.com/langgenius/dify/issues/43134) — Keyset pagination on (created_at, id) makes message ordering deterministic so tied timestamps never drop a chat message.
- [`state_persist/dify_runs_paginator.py`](src/llm_agent_dropin_fixes/state_persist/dify_runs_paginator.py) — [langgenius/dify #43265](https://github.com/langgenius/dify/issues/43265) — Keyset pagination on (created_at, id) makes workflow-run ordering deterministic so tied timestamps never skip a run.
- [`state_persist/dify_followup_resolver.py`](src/llm_agent_dropin_fixes/state_persist/dify_followup_resolver.py) — [langgenius/dify #43289](https://github.com/langgenius/dify/issues/43289) — Resolves anaphoric follow-ups to the anchor turn's slot so memory can seed the resolved query instead of raw sys.query.
- [`state_persist/mem0_orphan_msgs_audit.py`](src/llm_agent_dropin_fixes/state_persist/mem0_orphan_msgs_audit.py) — [mem0ai/mem0 #7452](https://github.com/mem0ai/mem0/issues/7452) — 突破组件：量化 delete_all() 之后残留的会话消息条数，定位会被下次 add() 重新喂给 LLM 并复提取的数据残留。
- [`state_persist/mem0_credential_suffix_probe.py`](src/llm_agent_dropin_fixes/state_persist/mem0_credential_suffix_probe.py) — [mem0ai/mem0 #7490](https://github.com/mem0ai/mem0/issues/7490) — 突破组件：识别被 _credential 后缀误判为敏感而红化的非凭据字段（如 use_azure_credential 布尔开关），防止 AzureMySQLConfig 重建静默降级。
- [`state_persist/mem0_history_resort.py`](src/llm_agent_dropin_fixes/state_persist/mem0_history_resort.py) — [mem0ai/mem0 #7502](https://github.com/mem0ai/mem0/issues/7502) — 突破组件：把 mem0 history() 的字符串比较改成按真实 UTC 偏移感知时间点排序，彻底消除跨时区审计顺序错乱。
- [`state_persist/mem0_cred_audit.py`](src/llm_agent_dropin_fixes/state_persist/mem0_cred_audit.py) — [mem0ai/mem0 #7504](https://github.com/mem0ai/mem0/issues/7504) — 突破组件：在任何 VectorStoreFactory.create() 之前审计 config 哪些凭据字段会被深拷贝红化清空，提前暴露 Elasticsearch 构造失败 / OpenSearch 匿名连接。
- [`state_persist/li_state_no_mutate.py`](src/llm_agent_dropin_fixes/state_persist/li_state_no_mutate.py) — [run-llama/llama_index #23234](https://github.com/run-llama/llama_index/issues/23234) — 用副本构建带 state 的临时 prompt，避免 setup_agent 把状态永久写进 memory 历史。
- [`state_persist/li_memory_mac.py`](src/llm_agent_dropin_fixes/state_persist/li_memory_mac.py) — [run-llama/llama_index #23246](https://github.com/run-llama/llama_index/issues/23246) — 对 memory 行计算 keyed MAC 并在 aget 校验，识别被篡改/重放的上下文行。
- [`state_persist/li_safe_pickle_check.py`](src/llm_agent_dropin_fixes/state_persist/li_safe_pickle_check.py) — [run-llama/llama_index #23256](https://github.com/run-llama/llama_index/issues/23256) — 在 persist 前校验对象是否落在上报允许清单，提前拒绝无法回载的对象。
- [`state_persist/cognee_notion_incremental.py`](src/llm_agent_dropin_fixes/state_persist/cognee_notion_incremental.py) — [topoteretes/cognee #4820](https://github.com/topoteretes/cognee/issues/4820) — 在保持每轮全量枚举（orphan_cleanup 安全）的前提下，用 last_edited_time 水位只重渲染变更页，降低 Notion 读取成本。
- [`state_persist/cognee_agentconn_lookup.py`](src/llm_agent_dropin_fixes/state_persist/cognee_agentconn_lookup.py) — [topoteretes/cognee #4909](https://github.com/topoteretes/cognee/issues/4909) — 把按名查找改为 active_only=False 后再筛名，使已停用连接返回 status:inactive 而非 404，止住插件轮询报错。
- [`state_persist/cognee_conn_badge_merge.py`](src/llm_agent_dropin_fixes/state_persist/cognee_conn_badge_merge.py) — [topoteretes/cognee #4957](https://github.com/topoteretes/cognee/issues/4957) — 把活跃注册连接（connections?active_only=true）并入连接状态判定，使新连接在无 session 行时立即显示 Connected。

### ctx_compact  (`ctx_compact/`) — 14 fixes

> 上下文压缩 / 客户端适配错乱：OpenRouter kwargs 误传、Langchain 兜底、嵌套属性序列化。

- [`ctx_compact/cline_github_mcp_device_flow.py`](src/llm_agent_dropin_fixes/ctx_compact/cline_github_mcp_device_flow.py) — [cline/cline #14625](https://github.com/cline/cline/issues/14625) — Implements the device-code grant GitHub supports, reachable when discovery 404s — the fallback Cline's ordering currently blocks (#14625).
- [`ctx_compact/cline_ctx_compactor.py`](src/llm_agent_dropin_fixes/ctx_compact/cline_ctx_compactor.py) — [cline/cline #14694](https://github.com/cline/cline/issues/14694) — Trims/summarizes oldest turns to a token budget so large-context sessions don't silently lose the Hub connection (#14694).
- [`ctx_compact/task_template_override.py`](src/llm_agent_dropin_fixes/ctx_compact/task_template_override.py) — [crewAIInc/crewAI #7766](https://github.com/crewAIInc/crewAI/issues/7766) — Targeted shim that swaps the hard-coded 'you MUST return...' line for the softer wording the MAST study argues for.
- [`ctx_compact/graphiti_max_tokens_resolve.py`](src/llm_agent_dropin_fixes/ctx_compact/graphiti_max_tokens_resolve.py) — [getzep/graphiti #1869](https://github.com/getzep/graphiti/issues/1869) — Consults the model's real output budget for extract_edges instead of the hard-coded 16384 cap.
- [`ctx_compact/graphiti_nested_attr_serialize.py`](src/llm_agent_dropin_fixes/ctx_compact/graphiti_nested_attr_serialize.py) — [getzep/graphiti #1885](https://github.com/getzep/graphiti/issues/1885) — Serializes legitimately nested attributes to JSON strings for all providers and drops only schema-echo shapes, preserving real data.
- [`ctx_compact/memary_context_entity_filter.py`](src/llm_agent_dropin_fixes/ctx_compact/memary_context_entity_filter.py) — [kingjulio8238/Memary #42](https://github.com/kingjulio8238/Memary/issues/42) — Filters Memary's top-N entities down to those literally/near-present in the agent's latest response, cutting irrelevant context tokens per the issue's ask.
- [`ctx_compact/view_image_bridge.py`](src/llm_agent_dropin_fixes/ctx_compact/view_image_bridge.py) — [labring/FastGPT #7827](https://github.com/labring/FastGPT/issues/7827) — 把工具/沙盒输出的图片 URL 或路径转成 image_url 内容块，补上 #7827 缺失的「图片作为下一轮模型输入」能力。
- [`ctx_compact/lc_bedrock_token_counter.py`](src/llm_agent_dropin_fixes/ctx_compact/lc_bedrock_token_counter.py) — [langchain-ai/langchain #40840](https://github.com/langchain-ai/langchain/issues/40840) — Recognizes Bedrock Claude token counts so SummarizationMiddleware compacts context before the window overflows, fixing the late-trigger gap.
- [`ctx_compact/dify_content_budget_probe.py`](src/llm_agent_dropin_fixes/ctx_compact/dify_content_budget_probe.py) — [langgenius/dify #43113](https://github.com/langgenius/dify/issues/43113) — Quantifies how much retrieved content is truncated under the 2000/12000 char limits so operators can pick sane values.
- [`ctx_compact/mem0_qdrant_paginate.py`](src/llm_agent_dropin_fixes/ctx_compact/mem0_qdrant_paginate.py) — [mem0ai/mem0 #7454](https://github.com/mem0ai/mem0/issues/7454) — 突破组件：把 Qdrant 单页 list() 改成跟随 offset 的全量滚动，消除实体存储/批量清理在 1 万行处静默截断。
- [`ctx_compact/mem0_langchain_list_shim.py`](src/llm_agent_dropin_fixes/ctx_compact/mem0_langchain_list_shim.py) — [mem0ai/mem0 #7461](https://github.com/mem0ai/mem0/issues/7461) — 突破组件：为 mem0 的 Langchain 向量存储补一个非 Chroma 兜底 list()，消除 FAISS/Qdrant/PGVector 下 get_all()/delete_all() 的 NoneType 崩溃。
- [`ctx_compact/mem0_openrouter_kwargs.py`](src/llm_agent_dropin_fixes/ctx_compact/mem0_openrouter_kwargs.py) — [mem0ai/mem0 #7469](https://github.com/mem0ai/mem0/issues/7469) — 突破组件：把 OpenRouter 的 models/route 字段正确塞进 extra_body 而非顶层 kwargs，消除每轮 LLM 调用前的 TypeError。
- [`ctx_compact/mem0_secret_log_filter.py`](src/llm_agent_dropin_fixes/ctx_compact/mem0_secret_log_filter.py) — [mem0ai/mem0 #7503](https://github.com/mem0ai/mem0/issues/7503) — 突破组件：给 mem0 的 vector store 日志加一层敏感字段过滤器，在不丢失字段名诊断价值的前提下遮蔽 service_account_json/private_key 等密钥。
- [`ctx_compact/li_refine_order_fix.py`](src/llm_agent_dropin_fixes/ctx_compact/li_refine_order_fix.py) — [run-llama/llama_index #23155](https://github.com/run-llama/llama_index/issues/23155) — 以反向入队恢复 FIFO 顺序，修正 Refine 对重排子块的反向折叠。

### rag_grounding  (`rag_grounding/`) — 8 fixes

> RAG 检索过滤错乱：Pinecone/Qdrant 过滤语法被包错、空 PDF 静默、重叠切片。

- [`rag_grounding/rag_type_probe.py`](src/llm_agent_dropin_fixes/rag_grounding/rag_type_probe.py) — [crewAIInc/crewAI #7827](https://github.com/crewAIInc/crewAI/issues/7827) — Per-item, case-normalized data_type detection that kills the outer-variable leakage and uppercase-extension misses in CrewAIRagAdapter.add().
- [`rag_grounding/graphiti_ingest_hygiene_hook.py`](src/llm_agent_dropin_fixes/rag_grounding/graphiti_ingest_hygiene_hook.py) — [getzep/graphiti #1880](https://github.com/getzep/graphiti/issues/1880) — Grounds extracted edges in source text via lexical overlap, flagging misattributed triples before commit.
- [`rag_grounding/dify_overlap_splitter.py`](src/llm_agent_dropin_fixes/rag_grounding/dify_overlap_splitter.py) — [langgenius/dify #43000](https://github.com/langgenius/dify/issues/43000) — Character-fallback splitter that holds a constant chunk_overlap on every boundary, fixing the alternating-overlap bug.
- [`rag_grounding/mem0_pgvector_bool_norm.py`](src/llm_agent_dropin_fixes/rag_grounding/mem0_pgvector_bool_norm.py) — [mem0ai/mem0 #7443](https://github.com/mem0ai/mem0/issues/7443) — 突破组件：把 pgvector 过滤值里的 Python 布尔归一为小写 JSON 文本，修复 eq/ne/in/nin 布尔过滤永不命中（及 ne/nin 静默返回被排除记录）的问题。
- [`rag_grounding/mem0_normalize_facts.py`](src/llm_agent_dropin_fixes/rag_grounding/mem0_normalize_facts.py) — [mem0ai/mem0 #7446](https://github.com/mem0ai/mem0/issues/7446) — 突破组件：修正 normalize_facts 对 {'facts':[...]} 整对象与裸字符串的误处理，避免事实抽取结果变成 ['facts'] 或逐字符列表。
- [`rag_grounding/mem0_qdrant_split_ops.py`](src/llm_agent_dropin_fixes/rag_grounding/mem0_qdrant_split_ops.py) — [mem0ai/mem0 #7468](https://github.com/mem0ai/mem0/issues/7468) — 突破组件：把合并在同一字段上的多个操作符拆成独立 AND 条件，修复 Qdrant 只应用首个操作符导致被排除记忆被返回的 bug。
- [`rag_grounding/mem0_pinecone_filter_fix.py`](src/llm_agent_dropin_fixes/rag_grounding/mem0_pinecone_filter_fix.py) — [mem0ai/mem0 #7483](https://github.com/mem0ai/mem0/issues/7483) — 突破组件：把 mem0 的 $or/$not 与 eq/in/ne 操作符正确翻译成 Pinecone 原生过滤语法，消除每类 OR/NOT 搜索的 HTTP 400。
- [`rag_grounding/li_qdrant_textkey_strip.py`](src/llm_agent_dropin_fixes/rag_grounding/li_qdrant_textkey_strip.py) — [run-llama/llama_index #23264](https://github.com/run-llama/llama_index/issues/23264) — 从 node.metadata 剥离 text_key，避免非 LlamaIndex 集合的 chunk 被重复送入 LLM。

### loop_guard  (`loop_guard/`) — 7 fixes

> 外部调用 / 生成循环失控：静默挂死、重复循环、缺超时重试与日志。

- [`loop_guard/gr_bounded_call_guard.py`](src/llm_agent_dropin_fixes/loop_guard/gr_bounded_call_guard.py) — [assafelovic/gpt-researcher #1764](https://github.com/assafelovic/gpt-researcher/issues/1764) — Thread-based bounded-call guard that turns silent external-call hangs into logged, retried, time-bounded events — directly answering the missing timeout/retry/logging ask.
- [`loop_guard/cline_stop_turn_isolator.py`](src/llm_agent_dropin_fixes/loop_guard/cline_stop_turn_isolator.py) — [cline/cline #14702](https://github.com/cline/cline/issues/14702) — Isolates each user turn behind a stop token so a follow-up cannot resume a cancelled stream — directly targets #14702.
- [`loop_guard/max_iter_guard.py`](src/llm_agent_dropin_fixes/loop_guard/max_iter_guard.py) — [crewAIInc/crewAI #7757](https://github.com/crewAIInc/crewAI/issues/7757) — Constructor guard that rejects max_iter < 1, turning the nonsense RecursionError into a clear validation error.
- [`loop_guard/flow_start_validator.py`](src/llm_agent_dropin_fixes/loop_guard/flow_start_validator.py) — [crewAIInc/crewAI #7758](https://github.com/crewAIInc/crewAI/issues/7758) — Static validator that fails fast when a Flow has no @start() entrypoint, preventing the silent None return.
- [`loop_guard/graphiti_repetition_loop_guard.py`](src/llm_agent_dropin_fixes/loop_guard/graphiti_repetition_loop_guard.py) — [getzep/graphiti #1922](https://github.com/getzep/graphiti/issues/1922) — Detects extract_edges repetition loops and re-rolls at higher temperature instead of resending the identical request.
- [`loop_guard/coop_stop_guard.py`](src/llm_agent_dropin_fixes/loop_guard/coop_stop_guard.py) — [labring/FastGPT #7665](https://github.com/labring/FastGPT/issues/7665) — 在工具执行期插入协作式停止检查与迭代上限，消除 #7665 指出的 base.ts:532 await 期间不检查停止信号的竞态。
- [`loop_guard/li_async_query_offload.py`](src/llm_agent_dropin_fixes/loop_guard/li_async_query_offload.py) — [run-llama/llama_index #23298](https://github.com/run-llama/llama_index/issues/23298) — 用 asyncio.to_thread 把同步 query 卸到线程，避免 aquery 阻塞事件循环。

### dedup  (`dedup/`) — 4 fixes

> 去重非确定性 / 重复抓取：tiebreak 不稳、shadow 重叠重复计。

- [`dedup/gr_shadow_overlap_meter.py`](src/llm_agent_dropin_fixes/dedup/gr_shadow_overlap_meter.py) — [assafelovic/gpt-researcher #2180](https://github.com/assafelovic/gpt-researcher/issues/2180) — Shadow-only overlap meter that proves or disproves duplicate paid scraping across parallel GPTResearcher branches without touching results or state.
- [`dedup/llm_failed_event_probe.py`](src/llm_agent_dropin_fixes/dedup/llm_failed_event_probe.py) — [crewAIInc/crewAI #7783](https://github.com/crewAIInc/crewAI/issues/7783) — Event-bus probe that counts LLMCallFailedEvent so the double-emission / scope-pop bug is reproducible in one run.
- [`dedup/graphiti_bulk_edge_dedup.py`](src/llm_agent_dropin_fixes/dedup/graphiti_bulk_edge_dedup.py) — [getzep/graphiti #1872](https://github.com/getzep/graphiti/issues/1872) — Merges identical facts across a bulk batch into one edge with combined episode uuids.
- [`dedup/graphiti_dedup_tiebreak.py`](src/llm_agent_dropin_fixes/dedup/graphiti_dedup_tiebreak.py) — [getzep/graphiti #1916](https://github.com/getzep/graphiti/issues/1916) — Breaks fuzzy-dedup ties on candidate uuid (sorted) so resolution is deterministic across processes.

### token_guard  (`token_guard/`) — 3 fixes

> token 计费 / 限流护栏：计数漏算、桶死锁、限流器形同虚设。

- [`token_guard/li_rate_limiter_guard.py`](src/llm_agent_dropin_fixes/token_guard/li_rate_limiter_guard.py) — [run-llama/llama_index #23202](https://github.com/run-llama/llama_index/issues/23202) — 对超出桶容量的请求快速失败而非死锁，修复 TokenBucket 永久阻塞与 SlidingWindow 放行超限。
- [`token_guard/li_dup_format_detect.py`](src/llm_agent_dropin_fixes/token_guard/li_dup_format_detect.py) — [run-llama/llama_index #23267](https://github.com/run-llama/llama_index/issues/23267) — 检测 prompt 中重复出现的 format 块，作为回归守卫捕捉多选提示被重复注入。
- [`token_guard/li_token_counter_fix.py`](src/llm_agent_dropin_fixes/token_guard/li_token_counter_fix.py) — [run-llama/llama_index #23313](https://github.com/run-llama/llama_index/issues/23313) — 对 tool_calls 同时兼容 dict 形态并对 None 名称/参数做护栏，消除 TokenCounter 漏算与 TypeError。

### other  (`probes/`) — 31 fixes

> 静默失效探针：代理路由、凭据、PDF 空提取等看不见的退化哨兵。

- [`probes/gr_pdf_silent_empty_probe.py`](src/llm_agent_dropin_fixes/probes/gr_pdf_silent_empty_probe.py) — [assafelovic/gpt-researcher #1582](https://github.com/assafelovic/gpt-researcher/issues/1582) — Silent-empty PDF extraction probe that catches scanned/image-only PDFs where the MIT pdfminer.six scraper yields empty context, pinpointing where an OCR fallback is needed.
- [`probes/cline_reasoning_validator.py`](src/llm_agent_dropin_fixes/probes/cline_reasoning_validator.py) — [cline/cline #14649](https://github.com/cline/cline/issues/14649) — Guards the reasoning level against each model's supported enum, preventing the Unsupported value commit-message error (#14649).
- [`probes/guardrail_llm_factory.py`](src/llm_agent_dropin_fixes/probes/guardrail_llm_factory.py) — [crewAIInc/crewAI #7764](https://github.com/crewAIInc/crewAI/issues/7764) — Factory that gives LLMGuardrail its own judge LLM, falling back to the agent's — your #7150 separation ask.
- [`probes/ztds_sanitizer.py`](src/llm_agent_dropin_fixes/probes/ztds_sanitizer.py) — [crewAIInc/crewAI #7789](https://github.com/crewAIInc/crewAI/issues/7789) — Local in-memory PII sanitizer with deterministic surrogates + length-ordered restore, zero network egress (ZTDS spirit).
- [`probes/graphiti_openai_mode_chooser.py`](src/llm_agent_dropin_fixes/probes/graphiti_openai_mode_chooser.py) — [getzep/graphiti #1874](https://github.com/getzep/graphiti/issues/1874) — Selects the OpenAI client from an explicit api_mode instead of hostname inference, supporting proxies.
- [`probes/graphiti_schema_require_all.py`](src/llm_agent_dropin_fixes/probes/graphiti_schema_require_all.py) — [getzep/graphiti #1909](https://github.com/getzep/graphiti/issues/1909) — Forces all json_schema properties required so grammar backends emit valid_at/invalid_at instead of omitting them.
- [`probes/graphiti_mcp_scope_expand.py`](src/llm_agent_dropin_fixes/probes/graphiti_mcp_scope_expand.py) — [getzep/graphiti #1919](https://github.com/getzep/graphiti/issues/1919) — Expands '*' to all groups and reports the searched scope so empty results aren't misread as 'no data'.
- [`probes/graphiti_prompt_order_probe.py`](src/llm_agent_dropin_fixes/probes/graphiti_prompt_order_probe.py) — [getzep/graphiti #1931](https://github.com/getzep/graphiti/issues/1931) — Diffs add_episode prompt output across PYTHONHASHSEED values to catch non-deterministic ordering regressions.
- [`probes/graphiti_mcp_arg_linter.py`](src/llm_agent_dropin_fixes/probes/graphiti_mcp_arg_linter.py) — [getzep/graphiti #1932](https://github.com/getzep/graphiti/issues/1932) — Validates MCP tool args against the declared schema and suggests the closest valid name for misspellings like group_id/group_ids.
- [`probes/graphiti_falkor_init_leak_probe.py`](src/llm_agent_dropin_fixes/probes/graphiti_falkor_init_leak_probe.py) — [getzep/graphiti #1934](https://github.com/getzep/graphiti/issues/1934) — Counts un-awaited build_indices_and_constraints tasks per group to expose the clone() task leak.
- [`probes/graphiti_llmcache_circular_safe.py`](src/llm_agent_dropin_fixes/probes/graphiti_llmcache_circular_safe.py) — [getzep/graphiti #1942](https://github.com/getzep/graphiti/issues/1942) — Catches ValueError (circular refs) in LLMCache.set so non-serializable values are skipped like TypeError cases.
- [`probes/graphiti_llmcache_threadsafe.py`](src/llm_agent_dropin_fixes/probes/graphiti_llmcache_threadsafe.py) — [getzep/graphiti #1944](https://github.com/getzep/graphiti/issues/1944) — Serializes LLMCache access with a lock so parallel set/get stop losing writes / returning wrong values.
- [`probes/graphiti_falkor6_index_probe.py`](src/llm_agent_dropin_fixes/probes/graphiti_falkor6_index_probe.py) — [getzep/graphiti #1947](https://github.com/getzep/graphiti/issues/1947) — Probes which FalkorDB createNodeIndex syntax the running server accepts, directly targeting the 6.0 'expected at most 1' break.
- [`probes/memary_parse_router.py`](src/llm_agent_dropin_fixes/probes/memary_parse_router.py) — [kingjulio8238/Memary #44](https://github.com/kingjulio8238/Memary/issues/44) — Implements the memaryParse parent router that dispatches by file extension and normalizes to TXT/MD/JSON, directly delivering issue #44's core design.
- [`probes/memary_external_memory_adapter.py`](src/llm_agent_dropin_fixes/probes/memary_external_memory_adapter.py) — [kingjulio8238/Memary #45](https://github.com/kingjulio8238/Memary/issues/45) — Wraps Memary behind a remember()/recall() adapter so it drops into any existing LLM chain as a standalone module, answering issue #45's integration question.
- [`probes/lc_tool_call_accumulator.py`](src/llm_agent_dropin_fixes/probes/lc_tool_call_accumulator.py) — [langchain-ai/langchain #40826](https://github.com/langchain-ai/langchain/issues/40826) — Buffers streamed tool-call argument deltas and parses the full JSON once, removing the per-chunk O(n^2) re-parse.
- [`probes/lc_limit_marker.py`](src/llm_agent_dropin_fixes/probes/lc_limit_marker.py) — [langchain-ai/langchain #40866](https://github.com/langchain-ai/langchain/issues/40866) — Tags middleware cutoff messages with a programmatic finish_reason marker so they're detectable without fragile English-text matching.
- [`probes/lc_typesafe_hardener.py`](src/llm_agent_dropin_fixes/probes/lc_typesafe_hardener.py) — [langchain-ai/langchain #40867](https://github.com/langchain-ai/langchain/issues/40867) — Pre-validates TypeSafe documented limits and retries 429/529 with backoff so production classify calls stop failing late.
- [`probes/lc_async_parallel_guard.py`](src/llm_agent_dropin_fixes/probes/lc_async_parallel_guard.py) — [langchain-ai/langchain #40877](https://github.com/langchain-ai/langchain/issues/40877) — Caps async branch concurrency with a semaphore so RunnableParallel-style fan-out respects max_concurrency on ainvoke/astream, preventing unbounded resource use.
- [`probes/lc_injected_arg_sanitizer.py`](src/llm_agent_dropin_fixes/probes/lc_injected_arg_sanitizer.py) — [langchain-ai/langchain #40880](https://github.com/langchain-ai/langchain/issues/40880) — Strips Pydantic-aliased injected tool args from on_tool_start serialized input so internal sentinels never reach callback logs.
- [`probes/lc_tool_error_kwargs.py`](src/llm_agent_dropin_fixes/probes/lc_tool_error_kwargs.py) — [langchain-ai/langchain #40881](https://github.com/langchain-ai/langchain/issues/40881) — Restores per-tool run context to on_tool_error by stashing on_tool_start kwargs per run_id and merging them back at error time.
- [`probes/dify_run_admission.py`](src/llm_agent_dropin_fixes/probes/dify_run_admission.py) — [langgenius/dify #43071](https://github.com/langgenius/dify/issues/43071) — Adds an explicit per-process capacity boundary for dify-agent runs via a semaphore, rejecting bursts with 429.
- [`probes/mem0_proxy_probe.py`](src/llm_agent_dropin_fixes/probes/mem0_proxy_probe.py) — [mem0ai/mem0 #7492](https://github.com/mem0ai/mem0/issues/7492) — 突破组件：用 httpx transport 类型探针确认各 provider 是否真的把 http_client_proxies 接通，暴露 17 个 provider 静默丢弃代理的隐患。
- [`probes/li_initrun_guard.py`](src/llm_agent_dropin_fixes/probes/li_initrun_guard.py) — [run-llama/llama_index #23153](https://github.com/run-llama/llama_index/issues/23153) — 在 user_hist 为空时安全回落到末条非 system 消息，消除 init_run 的 IndexError。
- [`probes/li_sql_schema_prefix.py`](src/llm_agent_dropin_fixes/probes/li_sql_schema_prefix.py) — [run-llama/llama_index #23301](https://github.com/run-llama/llama_index/issues/23301) — 对 SQL 字面量与注释先做掩码再仅对真实表引用加 schema 前缀，避免 FROM/JOIN 文本被改写。
- [`probes/cognee_neo4j_metrics.py`](src/llm_agent_dropin_fixes/probes/cognee_neo4j_metrics.py) — [topoteretes/cognee #4832](https://github.com/topoteretes/cognee/issues/4832) — 把全图 collect() 改写成 COUNT 轻量查询，并让 @deadlock_retry 跳过 MemoryPoolOutOfMemoryError，消除 OOM 重试风暴。
- [`probes/cognee_workflow_lint.py`](src/llm_agent_dropin_fixes/probes/cognee_workflow_lint.py) — [topoteretes/cognee #4865](https://github.com/topoteretes/cognee/issues/4865) — 本地扫描缺扩展名的工作流文件并校验 PR 标题语义类型，先把 #4865 的 pr_lint 改名 + 开启前自检。
- [`probes/cognee_subgraph_normalize.py`](src/llm_agent_dropin_fixes/probes/cognee_subgraph_normalize.py) — [topoteretes/cognee #5031](https://github.com/topoteretes/cognee/issues/5031) — 给出跨后端一致的 AND 分母（matched 而非 requested）、未知算子显式报错、无向边去重三处规范化实现。
- [`probes/cognee_provenance_acl.py`](src/llm_agent_dropin_fixes/probes/cognee_provenance_acl.py) — [topoteretes/cognee #5110](https://github.com/topoteretes/cognee/issues/5110) — 把 provenance 的数据集可见集改为按 ACL 授权计算，消除与 /visualize/brains 的口径分歧，修复空下拉。
- [`probes/cognee_contradiction_prefilter.py`](src/llm_agent_dropin_fixes/probes/cognee_contradiction_prefilter.py) — [topoteretes/cognee #5221](https://github.com/topoteretes/cognee/issues/5221) — 在 add_edges 前筛掉仅实体类型冲突（如 'qm is a person' vs 'qm is a feature'）的边，减少 ladybug UNREACHABLE_CODE 触发，保留事实性矛盾。
- [`probes/cognee_lancedb_xlock.py`](src/llm_agent_dropin_fixes/probes/cognee_lancedb_xlock.py) — [topoteretes/cognee #5254](https://github.com/topoteretes/cognee/issues/5254) — 跨进程 flock 把 LanceDB 的 create/merge_insert/delete 全量串行化，堵住 #5253 之外的跨进程写入竞争与重复向量 ID。

## Testing

```bash
pip install pytest
python -m pytest tests/ -q
```

- `tests/test_all_compile.py` — smoke gate: every one of the 109 modules compiles (syntax-valid, drop-in ready).
- `tests/test_flagship_examples.py` — correctness tests that **replay the bug then prove the fix**, for 4 representative fixes (cross-timezone sort, Pinecone L2→similarity, Pinecone filter translation, bounded-call hang guard).

## Disclaimer

Reference implementations only. Not affiliated with any upstream project. Verify against your own versions before shipping. MIT licensed.

## Collaboration — the 10% that isn't code

Read it, run it, fork it, and we will never chase you. This repo is the open part of a larger debug-engineering practice; below is exactly what is and isn't here so you can decide fast.

| Layer | What | Where |
|-------|------|-------|
| 🌱 Open | 109 reference fixes, 8 failure-taxonomy classes, full test suite, CI. | this repo |
| 🔑 Partner | Curated triage playbooks, the scoring/threshold config behind the taxonomies, and bespoke fix ports to your exact stack. | on request |
| 💎 Never shipped | Client code, private datasets, and anything that would expose a specific system's internals. | nowhere |

**Behind the lock.** The repo gives you the fixes; it does *not* give you (a) the prioritisation weights we use to pick which bug to attack first — those are tuned per client, and (b) the end-to-end runbooks that touch live credentials. None of that lives in this repo by design, and never will.

**How to ask.** Send two things: (1) what you're building and where the LLM-agent bug shows up, and (2) which layer you want and what you've already tried. A one-line message gets a one-line reply.

**Fit.** A fit: you run agents in production and hit one of the eight failure classes. Not a fit: you want us to debug your product for free. The sharpest failure modes reported as issues may land in the next release with credit.

Contact: hcac4735@agent.qq.com (SLA 48h). If that bounces overseas, open a GitHub issue instead.

