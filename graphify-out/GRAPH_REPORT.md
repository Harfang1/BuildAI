# Graph Report - .  (2026-11-20)

## Corpus Check
- Mise à jour incrémentale : old_server/ supprimé (199 nœuds retirés). Périmètre : app (server, scripts, fileserver, elasticsearch, racine), hors scrapping/raw_data.
- 0 files · ~3,300,876 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 283 nodes · 352 edges · 38 communities (28 shown, 10 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 21 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Orchestrateur avec logging|Orchestrateur avec logging]]
- [[_COMMUNITY_Routes API & schémas|Routes API & schémas]]
- [[_COMMUNITY_Docs & config déploiement|Docs & config déploiement]]
- [[_COMMUNITY_Moteur RAG & streaming|Moteur RAG & streaming]]
- [[_COMMUNITY_Retrieval hybride BM25+vecteur|Retrieval hybride BM25+vecteur]]
- [[_COMMUNITY_Indexation QdrantElasticsearch|Indexation Qdrant/Elasticsearch]]
- [[_COMMUNITY_Agent générateur de cours|Agent générateur de cours]]
- [[_COMMUNITY_Orchestrateur multi-agents|Orchestrateur multi-agents]]
- [[_COMMUNITY_Agent d'enrichissement|Agent d'enrichissement]]
- [[_COMMUNITY_Utilitaires LLM|Utilitaires LLM]]
- [[_COMMUNITY_Agent de recherche|Agent de recherche]]
- [[_COMMUNITY_API fileserver|API fileserver]]
- [[_COMMUNITY_Rapport raw data (racine)|Rapport raw data (racine)]]
- [[_COMMUNITY_Rapport raw data (scripts)|Rapport raw data (scripts)]]
- [[_COMMUNITY_Ingestion scrapping→Mongo|Ingestion scrapping→Mongo]]
- [[_COMMUNITY_Route RAG|Route RAG]]
- [[_COMMUNITY_Service streaming cours|Service streaming cours]]
- [[_COMMUNITY_Service streaming RAG|Service streaming RAG]]
- [[_COMMUNITY_Chargeur de config|Chargeur de config]]
- [[_COMMUNITY_Factory FastAPI|Factory FastAPI]]
- [[_COMMUNITY_Ingestion storage→Mongo|Ingestion storage→Mongo]]
- [[_COMMUNITY_Auth bearer token|Auth bearer token]]
- [[_COMMUNITY_Exemple génération cours|Exemple génération cours]]
- [[_COMMUNITY_Entrypoint Elasticsearch|Entrypoint Elasticsearch]]
- [[_COMMUNITY_Init package core|Init package core]]
- [[_COMMUNITY_Init package app|Init package app]]
- [[_COMMUNITY_Init package models|Init package models]]
- [[_COMMUNITY_Init package services|Init package services]]
- [[_COMMUNITY_PDF synthèse projet|PDF synthèse projet]]
- [[_COMMUNITY_Dépendances fileserver|Dépendances fileserver]]
- [[_COMMUNITY_Docker compose server|Docker compose server]]
- [[_COMMUNITY_Dépendances server|Dépendances server]]

## God Nodes (most connected - your core abstractions)
1. `MultiAgentOrchestratorWithLogging` - 13 edges
2. `CourseGeneratorAgent` - 12 edges
3. `LogCapture` - 12 edges
4. `KnowledgeEnhancerAgent` - 11 edges
5. `KnowledgeRetrieverAgent` - 10 edges
6. `MultiAgentOrchestrator` - 10 edges
7. `StreamingPrintCapture` - 10 edges
8. `stream_rag_with_thinking()` - 8 edges
9. `BuildAI User Stories Backlog` - 8 edges
10. `main()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `ChatRequest` --uses--> `ChatRequest`  [INFERRED]
  server/app/api/routes/rag.py → server/app/models/schemas.py
- `Legacy LibreChat Docker Compose Config` --semantically_similar_to--> `BuildAI Root Docker Compose Config`  [INFERRED] [semantically similar]
  C:/Users/adam_rkb/Documents/BUT INFO/BuildAI/dockerold.yml → C:/Users/adam_rkb/Documents/BUT INFO/BuildAI/docker-compose.yml
- `ChatRequest` --uses--> `ChatRequest`  [INFERRED]
  server/app/api/routes/course.py → server/app/models/schemas.py
- `MultiAgentOrchestrator` --uses--> `CourseGeneratorAgent`  [INFERRED]
  server/course_build_agents/orchestrator.py → server/course_build_agents/course_generator.py
- `LogCapture` --uses--> `CourseGeneratorAgent`  [INFERRED]
  server/course_build_agents/orchestrator_with_logging.py → server/course_build_agents/course_generator.py

## Import Cycles
- 1-file cycle: `scripts/index_mongo_to_elastic.py -> scripts/index_mongo_to_elastic.py`
- 1-file cycle: `server/app/main.py -> server/app/main.py`

## Hyperedges (group relationships)
- **Hybrid RAG Epic Documented Across Backlog, Synthesis & Architecture** — user_stories_backlog, user_stories_rag_hybride_concept, buildai_synthese_projet_overview, documentation_architecture_overview [INFERRED 0.80]
- **Docker Compose Variants Implementing GPU/CPU Fallback** — docker_compose_config, docker_compose_gpu_config, dockerold_config, docker_compose_gpu_cpu_fallback_concept [INFERRED 0.85]
- **Server Documentation Suite for Modular FastAPI Refactor** — server_readme_overview, documentation_architecture_overview, documentation_migration_guide_overview, documentation_streaming_architecture_overview [EXTRACTED 1.00]

## Communities (38 total, 10 thin omitted)

### Community 0 - "Orchestrateur avec logging"
Cohesion: 0.08
Nodes (19): LogCapture, main(), MultiAgentOrchestratorWithLogging, Captures print statements in a buffer for later retrieval., Captures both print statements and logging to a file and memory., Intercept stdout writes., Remove ANSI escape codes from text., Get all captured logs as string. (+11 more)

### Community 1 - "Routes API & schémas"
Cohesion: 0.09
Nodes (19): BaseModel, ChatRequest, course_chat(), course_download(), course_models(), Course generation endpoints router, List available course generation models, Course generation endpoint      Generates a complete course based on the subje (+11 more)

### Community 2 - "Docs & config déploiement"
Cohesion: 0.12
Nodes (23): BuildAI Project Synthesis (HTML/PDF), Converted User Stories (DOCX->MD), LibreChat Create User Command, BuildAI Root Docker Compose Config, Docker Compose GPU Override Config, GPU/CPU-RAM Fallback via Compose Override, Legacy LibreChat Docker Compose Config, Server Architecture Documentation (+15 more)

### Community 3 - "Moteur RAG & streaming"
Cohesion: 0.19
Nodes (13): Retourne le system prompt pour le RAG., Construit le prompt utilisateur avec la knowledge base et la question., Convertit [SOURCE X] en citations séquentielles [1](url), [2](url)..., Fonction principale pour interroger le système RAG., Stream RAG response from Ollama in real-time.     Yields status updates for rea, Récupère le contexte pertinent avec métadonnées pour citation., StreamingCitationFilter, add_citation_links() (+5 more)

### Community 4 - "Retrieval hybride BM25+vecteur"
Cohesion: 0.22
Nodes (13): Elasticsearch, _format_pdf_metadata(), Combine BM25 + vector results using RRF.     final_k: number of results to retu, Full hybrid pipeline:     - top_k BM25 candidates     - top_k vector candidate, ensure_index(), bm25_search(), _embed(), fetch_chunk() (+5 more)

### Community 5 - "Indexation Qdrant/Elasticsearch"
Cohesion: 0.19
Nodes (14): chunk_text(), ensure_es_index(), ensure_qdrant_collection(), extract_html_article(), get_embedding(), main(), normalize_and_lemmatize(), Path (+6 more)

### Community 6 - "Agent générateur de cours"
Cohesion: 0.18
Nodes (7): CourseGeneratorAgent, Generate detailed structure for each chapter with subchapters and content., Generate a complete course structure from the knowledge base., Generate markdown content as a string without saving to file., Export course structure to a readable markdown file., Generate high-level course outline., Agent 3: Generates comprehensive course structure.     Creates chapters, subcha

### Community 7 - "Orchestrateur multi-agents"
Cohesion: 0.21
Nodes (8): main(), MultiAgentOrchestrator, Orchestrates the three-agent system for course generation.          Flow:, Save knowledge base with sources to markdown file., Save complete results as JSON for programmatic access., Example usage of the multi-agent system., Initialize orchestrator with optional configuration.                  config e, Execute the complete multi-agent workflow.                  Args:

### Community 8 - "Agent d'enrichissement"
Cohesion: 0.21
Nodes (6): KnowledgeEnhancerAgent, Integrate new knowledge into existing knowledge base., Iteratively enhance knowledge by identifying and filling gaps., Identify gaps, unclear points, and missing information., Agent 2: Enhances knowledge by identifying gaps and filling them.     Asks clar, Fill identified gaps using RAG queries.

### Community 9 - "Utilitaires LLM"
Cohesion: 0.20
Nodes (10): add_citation_links(), call_llm(), call_llm_structured_output(), context_from_query(), fix_malformed_json(), Wrapper pour appeler le LLM avec system et user prompts., Failsafe function that asks LLM to fix malformed JSON.                  Args:, Récupère le contexte pertinent avec métadonnées pour citation. (+2 more)

### Community 10 - "Agent de recherche"
Cohesion: 0.24
Nodes (5): KnowledgeRetrieverAgent, Generate multiple search queries to cover the subject comprehensively., Retrieve and structure knowledge from multiple queries., Agent 1: Retrieves comprehensive knowledge on a subject.     Generates multiple, Synthesize retrieved knowledge into structured format.

### Community 11 - "API fileserver"
Cohesion: 0.32
Nodes (5): download_file(), find_file(), list_files(), Path, Download or view a PDF by filename, stem, or hash code.

### Community 12 - "Rapport raw data (racine)"
Cohesion: 0.54
Nodes (7): build_sibling_map(), detect_file_kind(), detect_source_for_file(), guess_source_from_text(), main(), Path, read_text_safe()

### Community 13 - "Rapport raw data (scripts)"
Cohesion: 0.54
Nodes (7): build_sibling_map(), detect_file_kind(), detect_source_for_file(), guess_source_from_text(), main(), Path, read_text_safe()

### Community 14 - "Ingestion scrapping→Mongo"
Cohesion: 0.57
Nodes (6): build_doc(), compute_hash(), connect_mongo(), get_file_type(), main(), Path

### Community 15 - "Route RAG"
Cohesion: 0.33
Nodes (5): ChatRequest, rag_chat(), rag_models(), List available RAG models, RAG chat completion endpoint      Supports both streaming and non-streaming re

### Community 16 - "Service streaming cours"
Cohesion: 0.40
Nodes (5): async_stream_wrapper_with_heartbeat(), Course generation service, Stream course generation with progress as reasoning_content      Args:, Wrapper to run a generator function and yield results asynchronously in real-tim, stream_course_generation()

### Community 17 - "Service streaming RAG"
Cohesion: 0.40
Nodes (5): async_rag_stream_wrapper(), RAG service for streaming responses, stream_rag_response(), Wrapper to run RAG streaming generator in real-time., Stream RAG response with instant feedback, real-time token streaming, and citati

### Community 18 - "Chargeur de config"
Cohesion: 0.33
Nodes (4): Config, Configuration loader for RAG server. Loads settings from config.ini and environ, Configuration class that combines config.ini and environment variables., Parse AUTH_TOKENS from environment variable.         Format: token1:user_id1:na

### Community 19 - "Factory FastAPI"
Cohesion: 0.50
Nodes (4): create_app(), Main FastAPI application factory, Create and configure the FastAPI application      Returns:         FastAPI: C, FastAPI

### Community 20 - "Ingestion storage→Mongo"
Cohesion: 0.67
Nodes (3): main(), process_file(), Path

### Community 21 - "Auth bearer token"
Cohesion: 0.50
Nodes (3): get_current_user(), Authentication and authorization, Verify bearer token and return user information      Args:         authorizat

## Knowledge Gaps
- **12 isolated node(s):** `entrypoint.sh script`, `Path`, `Synchronized Dual Indexing (Elasticsearch + Qdrant)`, `LibreChat Create User Command`, `Legacy LibreChat Docker Compose Config` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MultiAgentOrchestratorWithLogging` connect `Orchestrateur avec logging` to `Agent d'enrichissement`, `Routes API & schémas`, `Agent de recherche`, `Agent générateur de cours`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `CourseGeneratorAgent` connect `Agent générateur de cours` to `Orchestrateur avec logging`, `Orchestrateur multi-agents`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `ChatRequest` connect `Routes API & schémas` to `Route RAG`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `MultiAgentOrchestratorWithLogging` (e.g. with `CourseGeneratorAgent` and `KnowledgeEnhancerAgent`) actually correct?**
  _`MultiAgentOrchestratorWithLogging` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `CourseGeneratorAgent` (e.g. with `MultiAgentOrchestrator` and `LogCapture`) actually correct?**
  _`CourseGeneratorAgent` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `LogCapture` (e.g. with `CourseGeneratorAgent` and `KnowledgeEnhancerAgent`) actually correct?**
  _`LogCapture` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `KnowledgeEnhancerAgent` (e.g. with `MultiAgentOrchestrator` and `LogCapture`) actually correct?**
  _`KnowledgeEnhancerAgent` has 4 INFERRED edges - model-reasoned connections that need verification._