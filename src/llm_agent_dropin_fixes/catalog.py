# Auto-generated catalog of all drop-in fixes. Edit at your own risk.
CATALOG = [
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.mem0_history_resort",
  "repo": "mem0ai/mem0",
  "number": 7502,
  "issue": "https://github.com/mem0ai/mem0/issues/7502",
  "claim": "突破组件：把 mem0 history() 的字符串比较改成按真实 UTC 偏移感知时间点排序，彻底消除跨时区审计顺序错乱。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.mem0_cred_audit",
  "repo": "mem0ai/mem0",
  "number": 7504,
  "issue": "https://github.com/mem0ai/mem0/issues/7504",
  "claim": "突破组件：在任何 VectorStoreFactory.create() 之前审计 config 哪些凭据字段会被深拷贝红化清空，提前暴露 Elasticsearch 构造失败 / OpenSearch 匿名连接。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.mem0_credential_suffix_probe",
  "repo": "mem0ai/mem0",
  "number": 7490,
  "issue": "https://github.com/mem0ai/mem0/issues/7490",
  "claim": "突破组件：识别被 _credential 后缀误判为敏感而红化的非凭据字段（如 use_azure_credential 布尔开关），防止 AzureMySQLConfig 重建静默降级。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.mem0_orphan_msgs_audit",
  "repo": "mem0ai/mem0",
  "number": 7452,
  "issue": "https://github.com/mem0ai/mem0/issues/7452",
  "claim": "突破组件：量化 delete_all() 之后残留的会话消息条数，定位会被下次 add() 重新喂给 LLM 并复提取的数据残留。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.cognee_conn_badge_merge",
  "repo": "topoteretes/cognee",
  "number": 4957,
  "issue": "https://github.com/topoteretes/cognee/issues/4957",
  "claim": "把活跃注册连接（connections?active_only=true）并入连接状态判定，使新连接在无 session 行时立即显示 Connected。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.cognee_agentconn_lookup",
  "repo": "topoteretes/cognee",
  "number": 4909,
  "issue": "https://github.com/topoteretes/cognee/issues/4909",
  "claim": "把按名查找改为 active_only=False 后再筛名，使已停用连接返回 status:inactive 而非 404，止住插件轮询报错。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.cognee_notion_incremental",
  "repo": "topoteretes/cognee",
  "number": 4820,
  "issue": "https://github.com/topoteretes/cognee/issues/4820",
  "claim": "在保持每轮全量枚举（orphan_cleanup 安全）的前提下，用 last_edited_time 水位只重渲染变更页，降低 Notion 读取成本。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.graphiti_queue_retry",
  "repo": "getzep/graphiti",
  "number": 1911,
  "issue": "https://github.com/getzep/graphiti/issues/1911",
  "claim": "Retries transient ingest errors with backoff+jitter and re-queues episodes left with 0 edges."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.graphiti_secret_resolver",
  "repo": "getzep/graphiti",
  "number": 1887,
  "issue": "https://github.com/getzep/graphiti/issues/1887",
  "claim": "Resolves api_key from a file/callable/env/literal so rotating secrets stay out of env and config."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.graphiti_read_scope_resolver",
  "repo": "getzep/graphiti",
  "number": 1876,
  "issue": "https://github.com/getzep/graphiti/issues/1876",
  "claim": "Derives the read driver from group_id like _resolve_request_scope, so reads follow the write's database."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.graphiti_temporal_overlap",
  "repo": "getzep/graphiti",
  "number": 1865,
  "issue": "https://github.com/getzep/graphiti/issues/1865",
  "claim": "Checks validity-interval overlap before reusing a historical edge, preserving disjoint occurrences."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.lc_fallback_input_guard",
  "repo": "langchain-ai/langchain",
  "number": 40878,
  "issue": "https://github.com/langchain-ai/langchain/issues/40878",
  "claim": "Prevents with_fallbacks from corrupting the caller's input state by deep-copying before the fallback path runs."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.li_memory_mac",
  "repo": "run-llama/llama_index",
  "number": 23246,
  "issue": "https://github.com/run-llama/llama_index/issues/23246",
  "claim": "对 memory 行计算 keyed MAC 并在 aget 校验，识别被篡改/重放的上下文行。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.li_safe_pickle_check",
  "repo": "run-llama/llama_index",
  "number": 23256,
  "issue": "https://github.com/run-llama/llama_index/issues/23256",
  "claim": "在 persist 前校验对象是否落在上报允许清单，提前拒绝无法回载的对象。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.li_state_no_mutate",
  "repo": "run-llama/llama_index",
  "number": 23234,
  "issue": "https://github.com/run-llama/llama_index/issues/23234",
  "claim": "用副本构建带 state 的临时 prompt，避免 setup_agent 把状态永久写进 memory 历史。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.sqlite_wal_retry",
  "repo": "crewAIInc/crewAI",
  "number": 7822,
  "issue": "https://github.com/crewAIInc/crewAI/issues/7822",
  "claim": "Bounded exponential-backoff wrapper around PRAGMA journal_mode=WAL that removes the 'database is locked' race the maintainer's PR #7821 targets."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.from_cache_probe",
  "repo": "crewAIInc/crewAI",
  "number": 7775,
  "issue": "https://github.com/crewAIInc/crewAI/issues/7775",
  "claim": "Cache-tagged tool wrapper that emits ToolUsageFinishedEvent(from_cache=True) on replays, fixing the silent provenance bug."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.kickoff_storage_shim",
  "repo": "crewAIInc/crewAI",
  "number": 7746,
  "issue": "https://github.com/crewAIInc/crewAI/issues/7746",
  "claim": "Storage shim that serializes any JSON-able value on update and tolerates NULL on load, fixing the crash in KickoffTaskOutputsSQLiteStorage."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.dify_followup_resolver",
  "repo": "langgenius/dify",
  "number": 43289,
  "issue": "https://github.com/langgenius/dify/issues/43289",
  "claim": "Resolves anaphoric follow-ups to the anchor turn's slot so memory can seed the resolved query instead of raw sys.query."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.dify_logs_paginator",
  "repo": "langgenius/dify",
  "number": 43134,
  "issue": "https://github.com/langgenius/dify/issues/43134",
  "claim": "Keyset pagination on (created_at, id) makes message ordering deterministic so tied timestamps never drop a chat message."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.dify_runs_paginator",
  "repo": "langgenius/dify",
  "number": 43265,
  "issue": "https://github.com/langgenius/dify/issues/43265",
  "claim": "Keyset pagination on (created_at, id) makes workflow-run ordering deterministic so tied timestamps never skip a run."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.dify_vars_paginator",
  "repo": "langgenius/dify",
  "number": 43084,
  "issue": "https://github.com/langgenius/dify/issues/43084",
  "claim": "Keyset pagination on (created_at, id) makes conversation-variable ordering deterministic so tied timestamps never skip a variable."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.egress_policy",
  "repo": "labring/FastGPT",
  "number": 7345,
  "issue": "https://github.com/labring/FastGPT/issues/7345",
  "claim": "用通配符域名匹配实现 allow/deny 出网策略（默认 deny=fail-closed）并做命中词脱敏，对应 #7345 的 1.5 通配符与 3.2 redact。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.train_queue_checkpoint",
  "repo": "labring/FastGPT",
  "number": 7879,
  "issue": "https://github.com/labring/FastGPT/issues/7879",
  "claim": "把训练队列做成可暂停的 checkpoint 状态机，暂停时持久化已完成分块、恢复后从剩余继续，对应 #7879 的文档级/全局暂停与停止删除解耦。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.x402_detect",
  "repo": "labring/FastGPT",
  "number": 7837,
  "issue": "https://github.com/labring/FastGPT/issues/7837",
  "claim": "结构化识别 MCP 工具返回的 payment_required/payment_challenge，而非原样透传为文本，对应 #7837 的 detect it structurally 诉求。"
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.cline_orphan_daemon_reaper",
  "repo": "cline/cline",
  "number": 14700,
  "issue": "https://github.com/cline/cline/issues/14700",
  "claim": "Detects orphaned remote-helper daemons re-parented to init, giving the hub a concrete reaper hook for the leak/OOM in #14700."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.cline_perm_scope_auditor",
  "repo": "cline/cline",
  "number": 14699,
  "issue": "https://github.com/cline/cline/issues/14699",
  "claim": "Audits which settings scope grants a permission, surfacing the project-vs-user allow discrepancy behind the silent refusals in #14699."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.cline_models_auth_fetch",
  "repo": "cline/cline",
  "number": 14685,
  "issue": "https://github.com/cline/cline/issues/14685",
  "claim": "Shows the missing Bearer auth on the model-list fetch that fixes the HTTP 401 in #14685."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.cline_workspace_pruner",
  "repo": "cline/cline",
  "number": 14682,
  "issue": "https://github.com/cline/cline/issues/14682",
  "claim": "Prunes deleted folders from the persisted workspace list so the switcher stops showing dead entries (#14682)."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.cline_session_time_auditor",
  "repo": "cline/cline",
  "number": 14642,
  "issue": "https://github.com/cline/cline/issues/14642",
  "claim": "Flags sessions whose updatedAt resets to 'now' on launch without new activity, pinpointing the phantom-timestamp bug (#14642)."
 },
 {
  "category": "state_persist",
  "subpkg": "state_persist",
  "module": "state_persist.cline_mcp_orphan_reaper",
  "repo": "cline/cline",
  "number": 14622,
  "issue": "https://github.com/cline/cline/issues/14622",
  "claim": "Lists orphaned MCP server processes that outlive their session, giving the hub a reaper hook for /clear and quit (#14622)."
 },
 {
  "category": "rag_grounding",
  "subpkg": "rag_grounding",
  "module": "rag_grounding.mem0_pinecone_filter_fix",
  "repo": "mem0ai/mem0",
  "number": 7483,
  "issue": "https://github.com/mem0ai/mem0/issues/7483",
  "claim": "突破组件：把 mem0 的 $or/$not 与 eq/in/ne 操作符正确翻译成 Pinecone 原生过滤语法，消除每类 OR/NOT 搜索的 HTTP 400。"
 },
 {
  "category": "rag_grounding",
  "subpkg": "rag_grounding",
  "module": "rag_grounding.mem0_qdrant_split_ops",
  "repo": "mem0ai/mem0",
  "number": 7468,
  "issue": "https://github.com/mem0ai/mem0/issues/7468",
  "claim": "突破组件：把合并在同一字段上的多个操作符拆成独立 AND 条件，修复 Qdrant 只应用首个操作符导致被排除记忆被返回的 bug。"
 },
 {
  "category": "rag_grounding",
  "subpkg": "rag_grounding",
  "module": "rag_grounding.mem0_normalize_facts",
  "repo": "mem0ai/mem0",
  "number": 7446,
  "issue": "https://github.com/mem0ai/mem0/issues/7446",
  "claim": "突破组件：修正 normalize_facts 对 {'facts':[...]} 整对象与裸字符串的误处理，避免事实抽取结果变成 ['facts'] 或逐字符列表。"
 },
 {
  "category": "rag_grounding",
  "subpkg": "rag_grounding",
  "module": "rag_grounding.mem0_pgvector_bool_norm",
  "repo": "mem0ai/mem0",
  "number": 7443,
  "issue": "https://github.com/mem0ai/mem0/issues/7443",
  "claim": "突破组件：把 pgvector 过滤值里的 Python 布尔归一为小写 JSON 文本，修复 eq/ne/in/nin 布尔过滤永不命中（及 ne/nin 静默返回被排除记录）的问题。"
 },
 {
  "category": "rag_grounding",
  "subpkg": "rag_grounding",
  "module": "rag_grounding.graphiti_ingest_hygiene_hook",
  "repo": "getzep/graphiti",
  "number": 1880,
  "issue": "https://github.com/getzep/graphiti/issues/1880",
  "claim": "Grounds extracted edges in source text via lexical overlap, flagging misattributed triples before commit."
 },
 {
  "category": "rag_grounding",
  "subpkg": "rag_grounding",
  "module": "rag_grounding.li_qdrant_textkey_strip",
  "repo": "run-llama/llama_index",
  "number": 23264,
  "issue": "https://github.com/run-llama/llama_index/issues/23264",
  "claim": "从 node.metadata 剥离 text_key，避免非 LlamaIndex 集合的 chunk 被重复送入 LLM。"
 },
 {
  "category": "rag_grounding",
  "subpkg": "rag_grounding",
  "module": "rag_grounding.rag_type_probe",
  "repo": "crewAIInc/crewAI",
  "number": 7827,
  "issue": "https://github.com/crewAIInc/crewAI/issues/7827",
  "claim": "Per-item, case-normalized data_type detection that kills the outer-variable leakage and uppercase-extension misses in CrewAIRagAdapter.add()."
 },
 {
  "category": "rag_grounding",
  "subpkg": "rag_grounding",
  "module": "rag_grounding.dify_overlap_splitter",
  "repo": "langgenius/dify",
  "number": 43000,
  "issue": "https://github.com/langgenius/dify/issues/43000",
  "claim": "Character-fallback splitter that holds a constant chunk_overlap on every boundary, fixing the alternating-overlap bug."
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.mem0_pinecone_l2_rescore",
  "repo": "mem0ai/mem0",
  "number": 7482,
  "issue": "https://github.com/mem0ai/mem0/issues/7482",
  "claim": "突破组件：将 Pinecone 欧氏索引返回的 squared-distance 还原成单调递增相似度并重排，修复 Memory.search 在 L2 索引上丢最近记忆的问题。"
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.memary_synonym_retriever",
  "repo": "kingjulio8238/Memary",
  "number": 49,
  "issue": "https://github.com/kingjulio8238/Memary/issues/49",
  "claim": "Implements the LLMSynonymRetriever concept from issue #49: expands queries into synonyms then de-dupes retrieval hits to surface more relevant graph nodes."
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.cognee_recall_cutoff",
  "repo": "topoteretes/cognee",
  "number": 5222,
  "issue": "https://github.com/topoteretes/cognee/issues/5222",
  "claim": "对 recall 结果做融合分阈值截断 + 标识符型词法 boost，让噪声 prompt 返回空、commit SHA/工单号精确命中回到前列。"
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.cognee_triplet_backfill",
  "repo": "topoteretes/cognee",
  "number": 4822,
  "issue": "https://github.com/topoteretes/cognee/issues/4822",
  "claim": "从端点节点的 node_map 回填 belongs_to_set 到 Triplet/EdgeType 载荷，修复 node-set 过滤 triplet 检索恒为空 + 全表扫描。"
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.graphiti_node_distance_align",
  "repo": "getzep/graphiti",
  "number": 1897,
  "issue": "https://github.com/getzep/graphiti/issues/1897",
  "claim": "Pairs every returned edge with its source's node-distance score so shared-source facts aren't misaligned."
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.graphiti_episode_search_rerank",
  "repo": "getzep/graphiti",
  "number": 1888,
  "issue": "https://github.com/getzep/graphiti/issues/1888",
  "claim": "Reranks the full 2*limit candidate set before truncating to limit, so the cross-encoder sees all candidates."
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.li_choice_select_fix",
  "repo": "run-llama/llama_index",
  "number": 23273,
  "issue": "https://github.com/run-llama/llama_index/issues/23273",
  "claim": "将 choice-select 解析收紧到 1..num_choices 的 1-based 边界，杜绝 0/负数静默指向末节点。"
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.li_prevnext_score_fix",
  "repo": "run-llama/llama_index",
  "number": 23199,
  "issue": "https://github.com/run-llama/llama_index/issues/23199",
  "claim": "在邻居扩展后保留原始检索分数，防止 PrevNextNodePostprocessor 把已知分数覆盖成 None。"
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.dify_dsl_dataset_audit",
  "repo": "langgenius/dify",
  "number": 43062,
  "issue": "https://github.com/langgenius/dify/issues/43062",
  "claim": "Audits an imported workflow DSL for knowledge-retrieval nodes whose dataset_ids can't decrypt, converting a silent drop into a visible warning."
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.dify_hybrid_diagnostic",
  "repo": "langgenius/dify",
  "number": 42996,
  "issue": "https://github.com/langgenius/dify/issues/42996",
  "claim": "Detects the vectorizer:none misconfiguration and embeds the query client-side so hybrid retrieval returns chunks even before the rebuild."
 },
 {
  "category": "memory_rerank",
  "subpkg": "memory_rerank",
  "module": "memory_rerank.retrieval_trace",
  "repo": "labring/FastGPT",
  "number": 7113,
  "issue": "https://github.com/labring/FastGPT/issues/7113",
  "claim": "把 RAG 检索→重排→最终上下文做成可观测 trace，直接对应 #7113 的 Retrieval Trace View 诉求（retrieved/reranked/final_context/source attribution 四段）。"
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.mem0_openrouter_kwargs",
  "repo": "mem0ai/mem0",
  "number": 7469,
  "issue": "https://github.com/mem0ai/mem0/issues/7469",
  "claim": "突破组件：把 OpenRouter 的 models/route 字段正确塞进 extra_body 而非顶层 kwargs，消除每轮 LLM 调用前的 TypeError。"
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.mem0_langchain_list_shim",
  "repo": "mem0ai/mem0",
  "number": 7461,
  "issue": "https://github.com/mem0ai/mem0/issues/7461",
  "claim": "突破组件：为 mem0 的 Langchain 向量存储补一个非 Chroma 兜底 list()，消除 FAISS/Qdrant/PGVector 下 get_all()/delete_all() 的 NoneType 崩溃。"
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.mem0_qdrant_paginate",
  "repo": "mem0ai/mem0",
  "number": 7454,
  "issue": "https://github.com/mem0ai/mem0/issues/7454",
  "claim": "突破组件：把 Qdrant 单页 list() 改成跟随 offset 的全量滚动，消除实体存储/批量清理在 1 万行处静默截断。"
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.mem0_secret_log_filter",
  "repo": "mem0ai/mem0",
  "number": 7503,
  "issue": "https://github.com/mem0ai/mem0/issues/7503",
  "claim": "突破组件：给 mem0 的 vector store 日志加一层敏感字段过滤器，在不丢失字段名诊断价值的前提下遮蔽 service_account_json/private_key 等密钥。"
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.memary_context_entity_filter",
  "repo": "kingjulio8238/Memary",
  "number": 42,
  "issue": "https://github.com/kingjulio8238/Memary/issues/42",
  "claim": "Filters Memary's top-N entities down to those literally/near-present in the agent's latest response, cutting irrelevant context tokens per the issue's ask."
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.graphiti_nested_attr_serialize",
  "repo": "getzep/graphiti",
  "number": 1885,
  "issue": "https://github.com/getzep/graphiti/issues/1885",
  "claim": "Serializes legitimately nested attributes to JSON strings for all providers and drops only schema-echo shapes, preserving real data."
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.graphiti_max_tokens_resolve",
  "repo": "getzep/graphiti",
  "number": 1869,
  "issue": "https://github.com/getzep/graphiti/issues/1869",
  "claim": "Consults the model's real output budget for extract_edges instead of the hard-coded 16384 cap."
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.lc_bedrock_token_counter",
  "repo": "langchain-ai/langchain",
  "number": 40840,
  "issue": "https://github.com/langchain-ai/langchain/issues/40840",
  "claim": "Recognizes Bedrock Claude token counts so SummarizationMiddleware compacts context before the window overflows, fixing the late-trigger gap."
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.li_refine_order_fix",
  "repo": "run-llama/llama_index",
  "number": 23155,
  "issue": "https://github.com/run-llama/llama_index/issues/23155",
  "claim": "以反向入队恢复 FIFO 顺序，修正 Refine 对重排子块的反向折叠。"
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.task_template_override",
  "repo": "crewAIInc/crewAI",
  "number": 7766,
  "issue": "https://github.com/crewAIInc/crewAI/issues/7766",
  "claim": "Targeted shim that swaps the hard-coded 'you MUST return...' line for the softer wording the MAST study argues for."
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.dify_content_budget_probe",
  "repo": "langgenius/dify",
  "number": 43113,
  "issue": "https://github.com/langgenius/dify/issues/43113",
  "claim": "Quantifies how much retrieved content is truncated under the 2000/12000 char limits so operators can pick sane values."
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.view_image_bridge",
  "repo": "labring/FastGPT",
  "number": 7827,
  "issue": "https://github.com/labring/FastGPT/issues/7827",
  "claim": "把工具/沙盒输出的图片 URL 或路径转成 image_url 内容块，补上 #7827 缺失的「图片作为下一轮模型输入」能力。"
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.cline_ctx_compactor",
  "repo": "cline/cline",
  "number": 14694,
  "issue": "https://github.com/cline/cline/issues/14694",
  "claim": "Trims/summarizes oldest turns to a token budget so large-context sessions don't silently lose the Hub connection (#14694)."
 },
 {
  "category": "ctx_compact",
  "subpkg": "ctx_compact",
  "module": "ctx_compact.cline_github_mcp_device_flow",
  "repo": "cline/cline",
  "number": 14625,
  "issue": "https://github.com/cline/cline/issues/14625",
  "claim": "Implements the device-code grant GitHub supports, reachable when discovery 404s — the fallback Cline's ordering currently blocks (#14625)."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.mem0_proxy_probe",
  "repo": "mem0ai/mem0",
  "number": 7492,
  "issue": "https://github.com/mem0ai/mem0/issues/7492",
  "claim": "突破组件：用 httpx transport 类型探针确认各 provider 是否真的把 http_client_proxies 接通，暴露 17 个 provider 静默丢弃代理的隐患。"
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.gr_pdf_silent_empty_probe",
  "repo": "assafelovic/gpt-researcher",
  "number": 1582,
  "issue": "https://github.com/assafelovic/gpt-researcher/issues/1582",
  "claim": "Silent-empty PDF extraction probe that catches scanned/image-only PDFs where the MIT pdfminer.six scraper yields empty context, pinpointing where an OCR fallback is needed."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.memary_external_memory_adapter",
  "repo": "kingjulio8238/Memary",
  "number": 45,
  "issue": "https://github.com/kingjulio8238/Memary/issues/45",
  "claim": "Wraps Memary behind a remember()/recall() adapter so it drops into any existing LLM chain as a standalone module, answering issue #45's integration question."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.memary_parse_router",
  "repo": "kingjulio8238/Memary",
  "number": 44,
  "issue": "https://github.com/kingjulio8238/Memary/issues/44",
  "claim": "Implements the memaryParse parent router that dispatches by file extension and normalizes to TXT/MD/JSON, directly delivering issue #44's core design."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.cognee_lancedb_xlock",
  "repo": "topoteretes/cognee",
  "number": 5254,
  "issue": "https://github.com/topoteretes/cognee/issues/5254",
  "claim": "跨进程 flock 把 LanceDB 的 create/merge_insert/delete 全量串行化，堵住 #5253 之外的跨进程写入竞争与重复向量 ID。"
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.cognee_contradiction_prefilter",
  "repo": "topoteretes/cognee",
  "number": 5221,
  "issue": "https://github.com/topoteretes/cognee/issues/5221",
  "claim": "在 add_edges 前筛掉仅实体类型冲突（如 'qm is a person' vs 'qm is a feature'）的边，减少 ladybug UNREACHABLE_CODE 触发，保留事实性矛盾。"
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.cognee_provenance_acl",
  "repo": "topoteretes/cognee",
  "number": 5110,
  "issue": "https://github.com/topoteretes/cognee/issues/5110",
  "claim": "把 provenance 的数据集可见集改为按 ACL 授权计算，消除与 /visualize/brains 的口径分歧，修复空下拉。"
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.cognee_subgraph_normalize",
  "repo": "topoteretes/cognee",
  "number": 5031,
  "issue": "https://github.com/topoteretes/cognee/issues/5031",
  "claim": "给出跨后端一致的 AND 分母（matched 而非 requested）、未知算子显式报错、无向边去重三处规范化实现。"
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.cognee_workflow_lint",
  "repo": "topoteretes/cognee",
  "number": 4865,
  "issue": "https://github.com/topoteretes/cognee/issues/4865",
  "claim": "本地扫描缺扩展名的工作流文件并校验 PR 标题语义类型，先把 #4865 的 pr_lint 改名 + 开启前自检。"
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.cognee_neo4j_metrics",
  "repo": "topoteretes/cognee",
  "number": 4832,
  "issue": "https://github.com/topoteretes/cognee/issues/4832",
  "claim": "把全图 collect() 改写成 COUNT 轻量查询，并让 @deadlock_retry 跳过 MemoryPoolOutOfMemoryError，消除 OOM 重试风暴。"
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.graphiti_falkor6_index_probe",
  "repo": "getzep/graphiti",
  "number": 1947,
  "issue": "https://github.com/getzep/graphiti/issues/1947",
  "claim": "Probes which FalkorDB createNodeIndex syntax the running server accepts, directly targeting the 6.0 'expected at most 1' break."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.graphiti_llmcache_threadsafe",
  "repo": "getzep/graphiti",
  "number": 1944,
  "issue": "https://github.com/getzep/graphiti/issues/1944",
  "claim": "Serializes LLMCache access with a lock so parallel set/get stop losing writes / returning wrong values."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.graphiti_llmcache_circular_safe",
  "repo": "getzep/graphiti",
  "number": 1942,
  "issue": "https://github.com/getzep/graphiti/issues/1942",
  "claim": "Catches ValueError (circular refs) in LLMCache.set so non-serializable values are skipped like TypeError cases."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.graphiti_falkor_init_leak_probe",
  "repo": "getzep/graphiti",
  "number": 1934,
  "issue": "https://github.com/getzep/graphiti/issues/1934",
  "claim": "Counts un-awaited build_indices_and_constraints tasks per group to expose the clone() task leak."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.graphiti_mcp_arg_linter",
  "repo": "getzep/graphiti",
  "number": 1932,
  "issue": "https://github.com/getzep/graphiti/issues/1932",
  "claim": "Validates MCP tool args against the declared schema and suggests the closest valid name for misspellings like group_id/group_ids."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.graphiti_prompt_order_probe",
  "repo": "getzep/graphiti",
  "number": 1931,
  "issue": "https://github.com/getzep/graphiti/issues/1931",
  "claim": "Diffs add_episode prompt output across PYTHONHASHSEED values to catch non-deterministic ordering regressions."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.graphiti_mcp_scope_expand",
  "repo": "getzep/graphiti",
  "number": 1919,
  "issue": "https://github.com/getzep/graphiti/issues/1919",
  "claim": "Expands '*' to all groups and reports the searched scope so empty results aren't misread as 'no data'."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.graphiti_schema_require_all",
  "repo": "getzep/graphiti",
  "number": 1909,
  "issue": "https://github.com/getzep/graphiti/issues/1909",
  "claim": "Forces all json_schema properties required so grammar backends emit valid_at/invalid_at instead of omitting them."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.graphiti_openai_mode_chooser",
  "repo": "getzep/graphiti",
  "number": 1874,
  "issue": "https://github.com/getzep/graphiti/issues/1874",
  "claim": "Selects the OpenAI client from an explicit api_mode instead of hostname inference, supporting proxies."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.lc_async_parallel_guard",
  "repo": "langchain-ai/langchain",
  "number": 40877,
  "issue": "https://github.com/langchain-ai/langchain/issues/40877",
  "claim": "Caps async branch concurrency with a semaphore so RunnableParallel-style fan-out respects max_concurrency on ainvoke/astream, preventing unbounded resource use."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.lc_tool_error_kwargs",
  "repo": "langchain-ai/langchain",
  "number": 40881,
  "issue": "https://github.com/langchain-ai/langchain/issues/40881",
  "claim": "Restores per-tool run context to on_tool_error by stashing on_tool_start kwargs per run_id and merging them back at error time."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.lc_injected_arg_sanitizer",
  "repo": "langchain-ai/langchain",
  "number": 40880,
  "issue": "https://github.com/langchain-ai/langchain/issues/40880",
  "claim": "Strips Pydantic-aliased injected tool args from on_tool_start serialized input so internal sentinels never reach callback logs."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.lc_tool_call_accumulator",
  "repo": "langchain-ai/langchain",
  "number": 40826,
  "issue": "https://github.com/langchain-ai/langchain/issues/40826",
  "claim": "Buffers streamed tool-call argument deltas and parses the full JSON once, removing the per-chunk O(n^2) re-parse."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.lc_limit_marker",
  "repo": "langchain-ai/langchain",
  "number": 40866,
  "issue": "https://github.com/langchain-ai/langchain/issues/40866",
  "claim": "Tags middleware cutoff messages with a programmatic finish_reason marker so they're detectable without fragile English-text matching."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.lc_typesafe_hardener",
  "repo": "langchain-ai/langchain",
  "number": 40867,
  "issue": "https://github.com/langchain-ai/langchain/issues/40867",
  "claim": "Pre-validates TypeSafe documented limits and retries 429/529 with backoff so production classify calls stop failing late."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.li_sql_schema_prefix",
  "repo": "run-llama/llama_index",
  "number": 23301,
  "issue": "https://github.com/run-llama/llama_index/issues/23301",
  "claim": "对 SQL 字面量与注释先做掩码再仅对真实表引用加 schema 前缀，避免 FROM/JOIN 文本被改写。"
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.li_initrun_guard",
  "repo": "run-llama/llama_index",
  "number": 23153,
  "issue": "https://github.com/run-llama/llama_index/issues/23153",
  "claim": "在 user_hist 为空时安全回落到末条非 system 消息，消除 init_run 的 IndexError。"
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.ztds_sanitizer",
  "repo": "crewAIInc/crewAI",
  "number": 7789,
  "issue": "https://github.com/crewAIInc/crewAI/issues/7789",
  "claim": "Local in-memory PII sanitizer with deterministic surrogates + length-ordered restore, zero network egress (ZTDS spirit)."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.guardrail_llm_factory",
  "repo": "crewAIInc/crewAI",
  "number": 7764,
  "issue": "https://github.com/crewAIInc/crewAI/issues/7764",
  "claim": "Factory that gives LLMGuardrail its own judge LLM, falling back to the agent's — your #7150 separation ask."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.dify_run_admission",
  "repo": "langgenius/dify",
  "number": 43071,
  "issue": "https://github.com/langgenius/dify/issues/43071",
  "claim": "Adds an explicit per-process capacity boundary for dify-agent runs via a semaphore, rejecting bursts with 429."
 },
 {
  "category": "other",
  "subpkg": "probes",
  "module": "probes.cline_reasoning_validator",
  "repo": "cline/cline",
  "number": 14649,
  "issue": "https://github.com/cline/cline/issues/14649",
  "claim": "Guards the reasoning level against each model's supported enum, preventing the Unsupported value commit-message error (#14649)."
 },
 {
  "category": "dedup",
  "subpkg": "dedup",
  "module": "dedup.gr_shadow_overlap_meter",
  "repo": "assafelovic/gpt-researcher",
  "number": 2180,
  "issue": "https://github.com/assafelovic/gpt-researcher/issues/2180",
  "claim": "Shadow-only overlap meter that proves or disproves duplicate paid scraping across parallel GPTResearcher branches without touching results or state."
 },
 {
  "category": "dedup",
  "subpkg": "dedup",
  "module": "dedup.graphiti_dedup_tiebreak",
  "repo": "getzep/graphiti",
  "number": 1916,
  "issue": "https://github.com/getzep/graphiti/issues/1916",
  "claim": "Breaks fuzzy-dedup ties on candidate uuid (sorted) so resolution is deterministic across processes."
 },
 {
  "category": "dedup",
  "subpkg": "dedup",
  "module": "dedup.graphiti_bulk_edge_dedup",
  "repo": "getzep/graphiti",
  "number": 1872,
  "issue": "https://github.com/getzep/graphiti/issues/1872",
  "claim": "Merges identical facts across a bulk batch into one edge with combined episode uuids."
 },
 {
  "category": "dedup",
  "subpkg": "dedup",
  "module": "dedup.llm_failed_event_probe",
  "repo": "crewAIInc/crewAI",
  "number": 7783,
  "issue": "https://github.com/crewAIInc/crewAI/issues/7783",
  "claim": "Event-bus probe that counts LLMCallFailedEvent so the double-emission / scope-pop bug is reproducible in one run."
 },
 {
  "category": "loop_guard",
  "subpkg": "loop_guard",
  "module": "loop_guard.gr_bounded_call_guard",
  "repo": "assafelovic/gpt-researcher",
  "number": 1764,
  "issue": "https://github.com/assafelovic/gpt-researcher/issues/1764",
  "claim": "Thread-based bounded-call guard that turns silent external-call hangs into logged, retried, time-bounded events — directly answering the missing timeout/retry/logging ask."
 },
 {
  "category": "loop_guard",
  "subpkg": "loop_guard",
  "module": "loop_guard.graphiti_repetition_loop_guard",
  "repo": "getzep/graphiti",
  "number": 1922,
  "issue": "https://github.com/getzep/graphiti/issues/1922",
  "claim": "Detects extract_edges repetition loops and re-rolls at higher temperature instead of resending the identical request."
 },
 {
  "category": "loop_guard",
  "subpkg": "loop_guard",
  "module": "loop_guard.li_async_query_offload",
  "repo": "run-llama/llama_index",
  "number": 23298,
  "issue": "https://github.com/run-llama/llama_index/issues/23298",
  "claim": "用 asyncio.to_thread 把同步 query 卸到线程，避免 aquery 阻塞事件循环。"
 },
 {
  "category": "loop_guard",
  "subpkg": "loop_guard",
  "module": "loop_guard.flow_start_validator",
  "repo": "crewAIInc/crewAI",
  "number": 7758,
  "issue": "https://github.com/crewAIInc/crewAI/issues/7758",
  "claim": "Static validator that fails fast when a Flow has no @start() entrypoint, preventing the silent None return."
 },
 {
  "category": "loop_guard",
  "subpkg": "loop_guard",
  "module": "loop_guard.max_iter_guard",
  "repo": "crewAIInc/crewAI",
  "number": 7757,
  "issue": "https://github.com/crewAIInc/crewAI/issues/7757",
  "claim": "Constructor guard that rejects max_iter < 1, turning the nonsense RecursionError into a clear validation error."
 },
 {
  "category": "loop_guard",
  "subpkg": "loop_guard",
  "module": "loop_guard.coop_stop_guard",
  "repo": "labring/FastGPT",
  "number": 7665,
  "issue": "https://github.com/labring/FastGPT/issues/7665",
  "claim": "在工具执行期插入协作式停止检查与迭代上限，消除 #7665 指出的 base.ts:532 await 期间不检查停止信号的竞态。"
 },
 {
  "category": "loop_guard",
  "subpkg": "loop_guard",
  "module": "loop_guard.cline_stop_turn_isolator",
  "repo": "cline/cline",
  "number": 14702,
  "issue": "https://github.com/cline/cline/issues/14702",
  "claim": "Isolates each user turn behind a stop token so a follow-up cannot resume a cancelled stream — directly targets #14702."
 },
 {
  "category": "token_guard",
  "subpkg": "token_guard",
  "module": "token_guard.li_token_counter_fix",
  "repo": "run-llama/llama_index",
  "number": 23313,
  "issue": "https://github.com/run-llama/llama_index/issues/23313",
  "claim": "对 tool_calls 同时兼容 dict 形态并对 None 名称/参数做护栏，消除 TokenCounter 漏算与 TypeError。"
 },
 {
  "category": "token_guard",
  "subpkg": "token_guard",
  "module": "token_guard.li_rate_limiter_guard",
  "repo": "run-llama/llama_index",
  "number": 23202,
  "issue": "https://github.com/run-llama/llama_index/issues/23202",
  "claim": "对超出桶容量的请求快速失败而非死锁，修复 TokenBucket 永久阻塞与 SlidingWindow 放行超限。"
 },
 {
  "category": "token_guard",
  "subpkg": "token_guard",
  "module": "token_guard.li_dup_format_detect",
  "repo": "run-llama/llama_index",
  "number": 23267,
  "issue": "https://github.com/run-llama/llama_index/issues/23267",
  "claim": "检测 prompt 中重复出现的 format 块，作为回归守卫捕捉多选提示被重复注入。"
 }
]
