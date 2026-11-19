# Graph Report - .  (2026-11-19)

## Corpus Check
- Note: the full repo detected 1113 files · ~3,313,921 words, which triggered the large-corpus warning. Per user choice (reused from prior run), this run was scoped to server/old_server/scripts/fileserver/elasticsearch + root-level files, excluding `scrapping/raw_data` (the scraped BTP course corpus). The actual corpus processed below is 96 files · ~84,054 words.

## Summary
- 482 nodes · 588 edges · 62 communities (44 shown, 18 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.58)
- Token cost: 89,528 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Course Orchestration & Logging|Course Orchestration & Logging]]
- [[_COMMUNITY_Course & RAG API Routes|Course & RAG API Routes]]
- [[_COMMUNITY_Logging Orchestrator (server)|Logging Orchestrator (server)]]
- [[_COMMUNITY_Legacy RAG Server & Schemas|Legacy RAG Server & Schemas]]
- [[_COMMUNITY_Project Docs & Deployment Configs|Project Docs & Deployment Configs]]
- [[_COMMUNITY_RAG Prompt & Streaming (server)|RAG Prompt & Streaming (server)]]
- [[_COMMUNITY_QdrantElasticsearch Indexing Script|Qdrant/Elasticsearch Indexing Script]]
- [[_COMMUNITY_Hybrid BM25+Vector Retrieval (old_server)|Hybrid BM25+Vector Retrieval (old_server)]]
- [[_COMMUNITY_Course Generator Agent (old_server)|Course Generator Agent (old_server)]]
- [[_COMMUNITY_Course Generator Agent (server)|Course Generator Agent (server)]]
- [[_COMMUNITY_Multi-Agent Orchestrator (old_server)|Multi-Agent Orchestrator (old_server)]]
- [[_COMMUNITY_RAG Query Engine (old_server)|RAG Query Engine (old_server)]]
- [[_COMMUNITY_Multi-Agent Orchestrator (server)|Multi-Agent Orchestrator (server)]]
- [[_COMMUNITY_Knowledge Enhancer Agent (old_server)|Knowledge Enhancer Agent (old_server)]]
- [[_COMMUNITY_Hybrid Retriever (server)|Hybrid Retriever (server)]]
- [[_COMMUNITY_Knowledge Enhancer Agent (server)|Knowledge Enhancer Agent (server)]]
- [[_COMMUNITY_LLM Utility Helpers (old_server)|LLM Utility Helpers (old_server)]]
- [[_COMMUNITY_LLM Utility Helpers (server)|LLM Utility Helpers (server)]]
- [[_COMMUNITY_Knowledge Retriever Agent (old_server)|Knowledge Retriever Agent (old_server)]]
- [[_COMMUNITY_File Server Download API|File Server Download API]]
- [[_COMMUNITY_Raw Data File Reporter (root)|Raw Data File Reporter (root)]]
- [[_COMMUNITY_Raw Data File Reporter (scripts)|Raw Data File Reporter (scripts)]]
- [[_COMMUNITY_Mongo Ingestion Script|Mongo Ingestion Script]]
- [[_COMMUNITY_Course Streaming Service (old_server)|Course Streaming Service (old_server)]]
- [[_COMMUNITY_RAG Streaming Service (old_server)|RAG Streaming Service (old_server)]]
- [[_COMMUNITY_Config Loader & Auth Tokens (old_server)|Config Loader & Auth Tokens (old_server)]]
- [[_COMMUNITY_Course Streaming Service (server)|Course Streaming Service (server)]]
- [[_COMMUNITY_RAG Streaming Service (server)|RAG Streaming Service (server)]]
- [[_COMMUNITY_Config Loader & Auth Tokens (server)|Config Loader & Auth Tokens (server)]]
- [[_COMMUNITY_FastAPI App Factory (old_server)|FastAPI App Factory (old_server)]]
- [[_COMMUNITY_FastAPI App Factory (server)|FastAPI App Factory (server)]]
- [[_COMMUNITY_Bearer Token Auth (old_server)|Bearer Token Auth (old_server)]]
- [[_COMMUNITY_Storage-to-Mongo Ingestion|Storage-to-Mongo Ingestion]]
- [[_COMMUNITY_Bearer Token Auth (server)|Bearer Token Auth (server)]]
- [[_COMMUNITY_Course Generation Example (old_server)|Course Generation Example (old_server)]]
- [[_COMMUNITY_Course Generation Example (server)|Course Generation Example (server)]]
- [[_COMMUNITY_Elasticsearch Entrypoint Script|Elasticsearch Entrypoint Script]]
- [[_COMMUNITY_Core Package Init (old_server)|Core Package Init (old_server)]]
- [[_COMMUNITY_App Package Init (old_server)|App Package Init (old_server)]]
- [[_COMMUNITY_Models Package Init (old_server)|Models Package Init (old_server)]]
- [[_COMMUNITY_Services Package Init (old_server)|Services Package Init (old_server)]]
- [[_COMMUNITY_Docker Compose Duplicate Pair|Docker Compose Duplicate Pair]]
- [[_COMMUNITY_Requirements.txt Duplicate Pair|Requirements.txt Duplicate Pair]]
- [[_COMMUNITY_Core Package Init (server)|Core Package Init (server)]]
- [[_COMMUNITY_App Package Init (server)|App Package Init (server)]]
- [[_COMMUNITY_Models Package Init (server)|Models Package Init (server)]]
- [[_COMMUNITY_Services Package Init (server)|Services Package Init (server)]]
- [[_COMMUNITY_PDF Rendering of Project Synthesis|PDF Rendering of Project Synthesis]]
- [[_COMMUNITY_Architecture Doc Duplicate (old_server)|Architecture Doc Duplicate (old_server)]]
- [[_COMMUNITY_Migration Guide Duplicate (old_server)|Migration Guide Duplicate (old_server)]]
- [[_COMMUNITY_Streaming Architecture Duplicate (old_server)|Streaming Architecture Duplicate (old_server)]]
- [[_COMMUNITY_Fileserver Requirements|Fileserver Requirements]]

## God Nodes (most connected - your core abstractions)
1. `CourseGeneratorAgent` - 16 edges
2. `KnowledgeEnhancerAgent` - 15 edges
3. `MultiAgentOrchestratorWithLogging` - 15 edges
4. `KnowledgeRetrieverAgent` - 14 edges
5. `LogCapture` - 12 edges
6. `LogCapture` - 12 edges
7. `MultiAgentOrchestratorWithLogging` - 11 edges
8. `MultiAgentOrchestrator` - 10 edges
9. `StreamingPrintCapture` - 10 edges
10. `MultiAgentOrchestrator` - 10 edges

## Surprising Connections (you probably didn't know these)
- `ChatRequest` --uses--> `ChatRequest`  [INFERRED]
  old_server/app/api/routes/course.py → server/app/models/schemas.py
- `ChatRequest` --uses--> `ChatRequest`  [INFERRED]
  old_server/app/api/routes/rag.py → server/app/models/schemas.py
- `MultiAgentOrchestrator` --uses--> `CourseGeneratorAgent`  [INFERRED]
  old_server/course_build_agents/orchestrator.py → server/course_build_agents/course_generator.py
- `MultiAgentOrchestrator` --uses--> `KnowledgeEnhancerAgent`  [INFERRED]
  old_server/course_build_agents/orchestrator.py → server/course_build_agents/knowledge_enhancer.py
- `MultiAgentOrchestrator` --uses--> `KnowledgeRetrieverAgent`  [INFERRED]
  old_server/course_build_agents/orchestrator.py → server/course_build_agents/knowledge_retriever.py

## Import Cycles
- 1-file cycle: `old_server/app/main.py -> old_server/app/main.py`
- 1-file cycle: `scripts/index_mongo_to_elastic.py -> scripts/index_mongo_to_elastic.py`
- 1-file cycle: `server/app/main.py -> server/app/main.py`

## Hyperedges (group relationships)
- **Hybrid RAG Epic Documented Across Backlog, Synthesis & Architecture** — user_stories_backlog, user_stories_rag_hybride_concept, buildai_synthese_projet_overview, documentation_architecture_overview [INFERRED 0.80]
- **Docker Compose Variants Implementing GPU/CPU Fallback** — docker_compose_config, docker_compose_gpu_config, dockerold_config, docker_compose_gpu_cpu_fallback_concept [INFERRED 0.85]
- **Server Documentation Suite for Modular FastAPI Refactor** — server_readme_overview, documentation_architecture_overview, documentation_migration_guide_overview, documentation_streaming_architecture_overview [EXTRACTED 1.00]

## Communities (62 total, 18 thin omitted)

### Community 0 - "Course Orchestration & Logging"
Cohesion: 0.06
Nodes (24): LogCapture, main(), MultiAgentOrchestratorWithLogging, Captures print statements in a buffer for later retrieval., Captures both print statements and logging to a file and memory., Intercept stdout writes., Remove ANSI escape codes from text., Get all captured logs as string. (+16 more)

### Community 1 - "Course & RAG API Routes"
Cohesion: 0.06
Nodes (30): ChatRequest, course_chat(), course_download(), course_models(), Course generation endpoints router, List available course generation models, Course generation endpoint      Generates a complete course based on the subje, Download generated course files      Args:         filename: Path to the file (+22 more)

### Community 2 - "Logging Orchestrator (server)"
Cohesion: 0.08
Nodes (19): LogCapture, main(), MultiAgentOrchestratorWithLogging, Captures print statements in a buffer for later retrieval., Captures both print statements and logging to a file and memory., Intercept stdout writes., Remove ANSI escape codes from text., Get all captured logs as string. (+11 more)

### Community 3 - "Legacy RAG Server & Schemas"
Cohesion: 0.09
Nodes (17): BaseModel, ChatMessage, ChatRequest, Pydantic models and schemas for API requests/responses, Chat completion request model, ChatMessage, ChatRequest, course_chat() (+9 more)

### Community 4 - "Project Docs & Deployment Configs"
Cohesion: 0.12
Nodes (24): BuildAI Project Synthesis (HTML/PDF), Converted User Stories (DOCX->MD), LibreChat Create User Command, BuildAI Root Docker Compose Config, Docker Compose GPU Override Config, GPU/CPU-RAM Fallback via Compose Override, Legacy LibreChat Docker Compose Config, Server Architecture Documentation (+16 more)

### Community 5 - "RAG Prompt & Streaming (server)"
Cohesion: 0.19
Nodes (13): Retourne le system prompt pour le RAG., Construit le prompt utilisateur avec la knowledge base et la question., Convertit [SOURCE X] en citations séquentielles [1](url), [2](url)..., Fonction principale pour interroger le système RAG., Stream RAG response from Ollama in real-time.     Yields status updates for rea, Récupère le contexte pertinent avec métadonnées pour citation., StreamingCitationFilter, add_citation_links() (+5 more)

### Community 6 - "Qdrant/Elasticsearch Indexing Script"
Cohesion: 0.19
Nodes (14): chunk_text(), ensure_es_index(), ensure_qdrant_collection(), extract_html_article(), get_embedding(), main(), normalize_and_lemmatize(), Path (+6 more)

### Community 7 - "Hybrid BM25+Vector Retrieval (old_server)"
Cohesion: 0.22
Nodes (12): Elasticsearch, bm25_search(), _embed(), fetch_chunk(), hybrid_re_rank(), normalize_and_lemmatize(), Clean markdown + lowercase + French lemmatization., retrieve() (+4 more)

### Community 8 - "Course Generator Agent (old_server)"
Cohesion: 0.18
Nodes (7): CourseGeneratorAgent, Generate detailed structure for each chapter with subchapters and content., Generate a complete course structure from the knowledge base., Generate markdown content as a string without saving to file., Export course structure to a readable markdown file., Generate high-level course outline., Agent 3: Generates comprehensive course structure.     Creates chapters, subcha

### Community 9 - "Course Generator Agent (server)"
Cohesion: 0.18
Nodes (7): CourseGeneratorAgent, Generate detailed structure for each chapter with subchapters and content., Generate a complete course structure from the knowledge base., Generate markdown content as a string without saving to file., Export course structure to a readable markdown file., Generate high-level course outline., Agent 3: Generates comprehensive course structure.     Creates chapters, subcha

### Community 10 - "Multi-Agent Orchestrator (old_server)"
Cohesion: 0.21
Nodes (8): main(), MultiAgentOrchestrator, Orchestrates the three-agent system for course generation.          Flow:, Save knowledge base with sources to markdown file., Save complete results as JSON for programmatic access., Example usage of the multi-agent system., Initialize orchestrator with optional configuration.                  config e, Execute the complete multi-agent workflow.                  Args:

### Community 11 - "RAG Query Engine (old_server)"
Cohesion: 0.26
Nodes (12): add_citation_links(), context_from_query(), get_system_prompt(), query_rag(), rag_user_prompt(), stream_rag_with_thinking(), Convertit [SOURCE X] en citations séquentielles [1](url), [2](url)..., Fonction principale pour interroger le système RAG. (+4 more)

### Community 12 - "Multi-Agent Orchestrator (server)"
Cohesion: 0.21
Nodes (8): main(), MultiAgentOrchestrator, Orchestrates the three-agent system for course generation.          Flow:, Save knowledge base with sources to markdown file., Save complete results as JSON for programmatic access., Example usage of the multi-agent system., Initialize orchestrator with optional configuration.                  config e, Execute the complete multi-agent workflow.                  Args:

### Community 13 - "Knowledge Enhancer Agent (old_server)"
Cohesion: 0.21
Nodes (6): KnowledgeEnhancerAgent, Integrate new knowledge into existing knowledge base., Iteratively enhance knowledge by identifying and filling gaps., Identify gaps, unclear points, and missing information., Agent 2: Enhances knowledge by identifying gaps and filling them.     Asks clar, Fill identified gaps using RAG queries.

### Community 14 - "Hybrid Retriever (server)"
Cohesion: 0.29
Nodes (11): _format_pdf_metadata(), Combine BM25 + vector results using RRF.     final_k: number of results to retu, Full hybrid pipeline:     - top_k BM25 candidates     - top_k vector candidate, bm25_search(), _embed(), fetch_chunk(), hybrid_re_rank(), normalize_and_lemmatize() (+3 more)

### Community 15 - "Knowledge Enhancer Agent (server)"
Cohesion: 0.21
Nodes (6): KnowledgeEnhancerAgent, Integrate new knowledge into existing knowledge base., Iteratively enhance knowledge by identifying and filling gaps., Identify gaps, unclear points, and missing information., Agent 2: Enhances knowledge by identifying gaps and filling them.     Asks clar, Fill identified gaps using RAG queries.

### Community 16 - "LLM Utility Helpers (old_server)"
Cohesion: 0.20
Nodes (10): add_citation_links(), call_llm(), call_llm_structured_output(), context_from_query(), fix_malformed_json(), Wrapper pour appeler le LLM avec system et user prompts., Failsafe function that asks LLM to fix malformed JSON.                  Args:, Récupère le contexte pertinent avec métadonnées pour citation. (+2 more)

### Community 17 - "LLM Utility Helpers (server)"
Cohesion: 0.20
Nodes (10): add_citation_links(), call_llm(), call_llm_structured_output(), context_from_query(), fix_malformed_json(), Wrapper pour appeler le LLM avec system et user prompts., Failsafe function that asks LLM to fix malformed JSON.                  Args:, Récupère le contexte pertinent avec métadonnées pour citation. (+2 more)

### Community 18 - "Knowledge Retriever Agent (old_server)"
Cohesion: 0.24
Nodes (5): KnowledgeRetrieverAgent, Generate multiple search queries to cover the subject comprehensively., Retrieve and structure knowledge from multiple queries., Agent 1: Retrieves comprehensive knowledge on a subject.     Generates multiple, Synthesize retrieved knowledge into structured format.

### Community 19 - "File Server Download API"
Cohesion: 0.32
Nodes (5): download_file(), find_file(), list_files(), Path, Download or view a PDF by filename, stem, or hash code.

### Community 20 - "Raw Data File Reporter (root)"
Cohesion: 0.54
Nodes (7): build_sibling_map(), detect_file_kind(), detect_source_for_file(), guess_source_from_text(), main(), Path, read_text_safe()

### Community 21 - "Raw Data File Reporter (scripts)"
Cohesion: 0.54
Nodes (7): build_sibling_map(), detect_file_kind(), detect_source_for_file(), guess_source_from_text(), main(), Path, read_text_safe()

### Community 22 - "Mongo Ingestion Script"
Cohesion: 0.57
Nodes (6): build_doc(), compute_hash(), connect_mongo(), get_file_type(), main(), Path

### Community 23 - "Course Streaming Service (old_server)"
Cohesion: 0.40
Nodes (5): async_stream_wrapper_with_heartbeat(), Course generation service, Stream course generation with progress as reasoning_content      Args:, Wrapper to run a generator function and yield results asynchronously in real-tim, stream_course_generation()

### Community 24 - "RAG Streaming Service (old_server)"
Cohesion: 0.40
Nodes (5): async_rag_stream_wrapper(), RAG service for streaming responses, stream_rag_response(), Stream RAG response with thinking from Ollama, then corrected final response, Wrapper to run RAG streaming generator in real-time.

### Community 25 - "Config Loader & Auth Tokens (old_server)"
Cohesion: 0.33
Nodes (4): Config, Configuration loader for RAG server. Loads settings from config.ini and environ, Configuration class that combines config.ini and environment variables., Parse AUTH_TOKENS from environment variable.         Format: token1:user_id1:na

### Community 26 - "Course Streaming Service (server)"
Cohesion: 0.40
Nodes (5): async_stream_wrapper_with_heartbeat(), Course generation service, Stream course generation with progress as reasoning_content      Args:, Wrapper to run a generator function and yield results asynchronously in real-tim, stream_course_generation()

### Community 27 - "RAG Streaming Service (server)"
Cohesion: 0.40
Nodes (5): async_rag_stream_wrapper(), RAG service for streaming responses, stream_rag_response(), Wrapper to run RAG streaming generator in real-time., Stream RAG response with instant feedback, real-time token streaming, and citati

### Community 28 - "Config Loader & Auth Tokens (server)"
Cohesion: 0.33
Nodes (4): Config, Configuration loader for RAG server. Loads settings from config.ini and environ, Configuration class that combines config.ini and environment variables., Parse AUTH_TOKENS from environment variable.         Format: token1:user_id1:na

### Community 29 - "FastAPI App Factory (old_server)"
Cohesion: 0.50
Nodes (4): create_app(), Main FastAPI application factory, Create and configure the FastAPI application      Returns:         FastAPI: C, FastAPI

### Community 30 - "FastAPI App Factory (server)"
Cohesion: 0.50
Nodes (4): create_app(), Main FastAPI application factory, Create and configure the FastAPI application      Returns:         FastAPI: C, FastAPI

### Community 31 - "Bearer Token Auth (old_server)"
Cohesion: 0.50
Nodes (3): get_current_user(), Authentication and authorization, Verify bearer token and return user information      Args:         authorizat

### Community 32 - "Storage-to-Mongo Ingestion"
Cohesion: 0.67
Nodes (3): main(), process_file(), Path

### Community 33 - "Bearer Token Auth (server)"
Cohesion: 0.50
Nodes (3): get_current_user(), Authentication and authorization, Verify bearer token and return user information      Args:         authorizat

## Knowledge Gaps
- **17 isolated node(s):** `entrypoint.sh script`, `Path`, `Synchronized Dual Indexing (Elasticsearch + Qdrant)`, `LibreChat Create User Command`, `Legacy LibreChat Docker Compose Config` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MultiAgentOrchestratorWithLogging` connect `Logging Orchestrator (server)` to `Course Orchestration & Logging`, `Course Generator Agent (server)`, `Legacy RAG Server & Schemas`, `Knowledge Enhancer Agent (server)`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `ChatRequest` connect `Course & RAG API Routes` to `Legacy RAG Server & Schemas`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `CourseGeneratorAgent` connect `Course Generator Agent (server)` to `Course Orchestration & Logging`, `Multi-Agent Orchestrator (old_server)`, `Logging Orchestrator (server)`, `Multi-Agent Orchestrator (server)`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `CourseGeneratorAgent` (e.g. with `MultiAgentOrchestrator` and `LogCapture`) actually correct?**
  _`CourseGeneratorAgent` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `KnowledgeEnhancerAgent` (e.g. with `MultiAgentOrchestrator` and `LogCapture`) actually correct?**
  _`KnowledgeEnhancerAgent` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `MultiAgentOrchestratorWithLogging` (e.g. with `ChatMessage` and `ChatRequest`) actually correct?**
  _`MultiAgentOrchestratorWithLogging` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `KnowledgeRetrieverAgent` (e.g. with `MultiAgentOrchestrator` and `LogCapture`) actually correct?**
  _`KnowledgeRetrieverAgent` has 8 INFERRED edges - model-reasoned connections that need verification._