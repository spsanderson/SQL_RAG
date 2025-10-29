# **Architecture Document: SQL RAG Ollama - Natural Language Database Query System**

**Project**: SQL RAG Ollama  
**Phase**: SPARC Phase 3 - Architecture  
**Version**: 1.0  
**Date**: October 29, 2025  
**Status**: Design Complete, Ready for Implementation

---

## **Executive Summary**

This architecture document defines the technical blueprint for the SQL RAG Ollama application—a natural language interface for SQL databases leveraging local Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG). The architecture supports the core objective: **enabling non-technical healthcare users to query databases through conversational language while maintaining HIPAA compliance through local-only processing**.

**Key Architectural Decisions**:
- **Style**: Modular Monolith with clean separation of concerns
- **Deployment**: Single-server with optional horizontal scaling
- **LLM Runtime**: Ollama (local inference, no external APIs)
- **Vector Store**: ChromaDB (embedded for simplicity)
- **Database**: SQL Server (extensible to PostgreSQL/MySQL)
- **UI Framework**: Streamlit (rapid development, Python-native)
- **Language**: Python 3.9+ (ecosystem maturity, ML libraries)

**Architecture Principles**:
1. **Privacy First**: All processing occurs locally; zero external API dependencies
2. **Simplicity Over Complexity**: Start with monolith; scale when needed
3. **Extensibility**: Plugin architecture for databases, LLMs, UI frameworks
4. **Fail-Safe Design**: Multiple validation layers prevent harmful operations
5. **Observable**: Comprehensive logging, metrics, and health monitoring

---

## **1. AI Model Utilization in Architecture Development**

### **1.1 Advanced AI Assistance (Architecture Phase)**

**Models Used**:
- **GPT-4 / Claude Sonnet 4.5**: Complex architectural problem-solving, design pattern recommendations
- **GitHub Copilot**: Code structure templates, boilerplate generation
- **Perplexity AI**: Research on architectural patterns, technology benchmarks

**Use Cases**:

**Architectural Pattern Selection**:
```
Query to AI: "Compare microservices vs modular monolith for a Python LLM 
application with 10-20 concurrent users, emphasizing local deployment and 
HIPAA compliance."

AI Response: [Analysis of trade-offs, recommendation for modular monolith
with rationale: lower operational complexity, adequate for scale, easier
HIPAA audit trail, simpler deployment]

Decision: Adopted modular monolith recommendation
```

**Technology Stack Evaluation**:
```
Query: "Evaluate Streamlit vs Flask vs FastAPI for Python web UI serving
an LLM query application. Consider: development speed, user session 
management, WebSocket support for streaming, deployment complexity."

AI Response: [Comparison matrix with pros/cons]

Decision: Streamlit for MVP (fastest development), with abstraction layer
enabling future FastAPI migration if needed
```

**Security Architecture**:
```
Query: "Design defense-in-depth security architecture for healthcare
SQL query system. Must prevent: SQL injection, unauthorized data access,
accidental data modification. Local deployment, no external APIs."

AI Response: [Multi-layer security design with validation gates]

Decision: Implemented 5-layer validation architecture (input → intent → 
SQL generation → validation → execution)
```

### **1.2 Cost-Effective AI for Documentation**

**GPT-3.5 / Claude Haiku** used for:
- Generating API documentation from code signatures
- Creating README templates
- Drafting error message copy
- Code comment generation

**Example**:
```python
# AI-generated docstring from function signature
def retrieve_schema_context(query: str, top_k: int = 5) -> List[SchemaElement]:
    """
    Retrieve relevant database schema elements for a given query.
    
    Uses semantic search against vector store to find tables, columns,
    and relationships most relevant to the user's natural language query.
    
    Args:
        query: Natural language query from user
        top_k: Number of schema elements to retrieve (default: 5)
        
    Returns:
        List of SchemaElement objects ranked by relevance
        
    Raises:
        VectorStoreError: If connection to vector store fails
        EmbeddingError: If query embedding generation fails
    """
```

### **1.3 AI Interaction Documentation**

**Knowledge Base Maintained**:

`docs/ai-assisted-decisions/`
```
001_architectural_style_selection.md
002_technology_stack_evaluation.md
003_rag_pipeline_design.md
004_security_validation_layers.md
005_prompt_engineering_strategies.md
```

Each file documents:
- Question posed to AI
- AI response summary
- Decision made
- Rationale for acceptance/rejection
- Date and context

**Benefits**:
- Audit trail for architectural decisions
- Onboarding resource for new team members
- Reference for similar future decisions
- Demonstrates due diligence for stakeholder reviews

---

## **2. Architectural Style Selection**

### **2.1 Evaluation of Architectural Styles**

**Styles Considered**:

#### **Option 1: Microservices Architecture**

**Description**: Decompose system into independently deployable services (LLM Service, RAG Service, Query Service, UI Service).

**Pros**:
- ✅ Independent scaling of components
- ✅ Technology flexibility per service
- ✅ Fault isolation (one service failure doesn't crash system)
- ✅ Team autonomy (separate teams per service)

**Cons**:
- ❌ Operational complexity (multiple deployments, monitoring)
- ❌ Network latency between services
- ❌ Distributed system challenges (transactions, consistency)
- ❌ Overhead excessive for 10-20 users
- ❌ HIPAA compliance audit complexity (multiple attack surfaces)

**Verdict**: **Rejected** - Complexity outweighs benefits at this scale.

---

#### **Option 2: Traditional Monolith**

**Description**: Single codebase, single deployment, tightly coupled components.

**Pros**:
- ✅ Simple deployment (one artifact)
- ✅ Easy local development
- ✅ Straightforward debugging
- ✅ Lower operational overhead

**Cons**:
- ❌ Scaling challenges (scale entire app, not components)
- ❌ Technology lock-in (Python everywhere)
- ❌ Tight coupling hinders maintenance
- ❌ Testing complexity (hard to isolate components)

**Verdict**: **Rejected** - Too rigid for future evolution.

---

#### **Option 3: Modular Monolith** ✅

**Description**: Single deployment with well-defined internal module boundaries, clean interfaces, and potential for future service extraction.

**Pros**:
- ✅ **Simplicity**: Single codebase, single deployment
- ✅ **Modularity**: Clear boundaries enable independent development
- ✅ **Performance**: In-process communication (no network overhead)
- ✅ **Evolution Path**: Modules can become services if needed
- ✅ **Testing**: Modules testable in isolation
- ✅ **HIPAA Compliance**: Single audit surface, easier to secure
- ✅ **Development Speed**: Shared code, no distributed system complexity
- ✅ **Operational Simplicity**: One process to monitor/deploy

**Cons**:
- ⚠️ Requires discipline to maintain boundaries
- ⚠️ Shared database can create coupling
- ⚠️ Scaling less granular than microservices

**Verdict**: **SELECTED** - Optimal balance for requirements and scale.

---

#### **Option 4: Event-Driven Architecture**

**Description**: Components communicate via message bus (e.g., RabbitMQ, Kafka).

**Pros**:
- ✅ Decoupled components
- ✅ Asynchronous processing
- ✅ Scalable event processing

**Cons**:
- ❌ Unnecessary complexity for synchronous query workflow
- ❌ Message broker adds infrastructure dependency
- ❌ Debugging challenges (trace events across components)
- ❌ Overkill for request-response pattern

**Verdict**: **Rejected** - Doesn't match usage pattern (users expect immediate response, not async).

---

### **2.2 Selection Criteria and Justification**

**Decision Matrix**:

| Criterion | Weight | Microservices | Monolith | Modular Monolith | Event-Driven |
|-----------|--------|---------------|----------|------------------|--------------|
| **Scalability to 20 users** | 15% | 8 | 9 | 9 | 7 |
| **Development Speed** | 20% | 5 | 9 | 8 | 6 |
| **Operational Simplicity** | 20% | 4 | 10 | 9 | 5 |
| **HIPAA Compliance Ease** | 15% | 6 | 9 | 9 | 7 |
| **Team Expertise Match** | 10% | 5 | 8 | 8 | 6 |
| **Future Extensibility** | 10% | 9 | 5 | 8 | 8 |
| **Performance** | 10% | 7 | 10 | 10 | 7 |
| **Total (Weighted)** | 100% | **6.15** | **8.65** | **8.60** | **6.55** |

**Winner**: Modular Monolith (score: 8.60) - Narrowly edges traditional monolith due to better extensibility while maintaining operational simplicity.

**Justification**:

**Why Modular Monolith Wins**:

1. **Right-Sized for Scale**: 10-20 concurrent users don't justify microservices overhead
2. **Operational Simplicity**: Healthcare IT teams prefer simple deployments; single process easier to monitor/maintain
3. **HIPAA Compliance**: Single attack surface; simpler security audit
4. **Development Velocity**: Team can iterate quickly without distributed system complexity
5. **Evolution Path**: Module boundaries enable future service extraction if scale demands
6. **Performance**: In-process calls faster than network calls (critical for <5s response target)

**Addressing Non-Functional Requirements**:

- **NFR-1 (Performance)**: ✅ No network latency between components
- **NFR-2 (Security)**: ✅ Single audit perimeter, centralized logging
- **NFR-3 (Reliability)**: ✅ Fewer moving parts = fewer failure modes
- **NFR-5 (Maintainability)**: ✅ Single codebase with clear module structure
- **NFR-7 (Scalability)**: ✅ Vertical scaling sufficient; horizontal if needed later

---

### **2.3 Modular Monolith Structure**

**Core Modules** (Independent Responsibilities):

```
sql-rag-ollama/
│
├── src/
│   ├── core/              # Business Logic Module
│   │   ├── query_processor.py       # Main orchestration
│   │   ├── conversation_manager.py  # Session management
│   │   └── intent_classifier.py     # NL intent parsing
│   │
│   ├── database/          # Data Access Module
│   │   ├── connection.py            # DB connectivity
│   │   ├── schema_loader.py         # Schema extraction
│   │   └── query_executor.py        # SQL execution
│   │
│   ├── llm/               # LLM Integration Module
│   │   ├── ollama_client.py         # Ollama API client
│   │   ├── prompt_builder.py        # Prompt construction
│   │   └── sql_parser.py            # Parse SQL from response
│   │
│   ├── rag/               # RAG Module
│   │   ├── vector_store.py          # ChromaDB interface
│   │   ├── embeddings.py            # Embedding generation
│   │   └── retriever.py             # Context retrieval
│   │
│   ├── validation/        # Security Module
│   │   ├── sql_validator.py         # SQL safety checks
│   │   ├── input_sanitizer.py       # Input validation
│   │   └── schema_validator.py      # Schema verification
│   │
│   └── ui/                # Presentation Module
│       ├── streamlit_app.py         # Web interface
│       └── components/              # Reusable UI components
```

**Module Communication**:
- **Interfaces**: Each module exposes clear Python interfaces (classes/functions)
- **Dependency Injection**: Modules receive dependencies at initialization (testable, mockable)
- **Event Bus** (Optional): Simple in-process event system for cross-module notifications
- **Shared Data**: Minimal; each module owns its data

**Boundary Enforcement**:
```python
# Module boundary example
# core/ module depends on database/, llm/, rag/, validation/
# but database/ CANNOT import from core/ (unidirectional dependency)

# Enforced via:
# 1. Import linters (pylint, flake8)
# 2. Architectural tests
# 3. Code review checklist
```

---

## **3. System Architecture Diagram**

### **3.1 High-Level System Context**

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL ACTORS                             │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
            ┌──────────┐  ┌──────────┐  ┌──────────┐
            │  End     │  │  Admin   │  │  API     │
            │  User    │  │  User    │  │  Client  │
            └────┬─────┘  └────┬─────┘  └────┬─────┘
                 │             │             │
                 │   HTTPS     │   HTTPS     │   HTTPS
                 │             │             │
                 └─────────────┼─────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SQL RAG OLLAMA APPLICATION                       │
│                       (Single Process)                              │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                    UI MODULE (Streamlit)                       │ │
│  │  • Web Interface  • Session Management  • Result Display      │ │
│  └───────────┬───────────────────────────────────────────────────┘ │
│              │                                                       │
│  ┌───────────▼───────────────────────────────────────────────────┐ │
│  │                    CORE MODULE (Orchestration)                 │ │
│  │  • Query Processor  • Intent Classifier  • Conversation Mgr   │ │
│  └─┬────────────────┬────────────────┬────────────────┬─────────┘ │
│    │                │                │                │            │
│    ▼                ▼                ▼                ▼            │
│  ┌────────┐   ┌────────┐      ┌────────┐      ┌──────────┐       │
│  │  RAG   │   │  LLM   │      │DATABASE│      │VALIDATION│       │
│  │ MODULE │   │ MODULE │      │ MODULE │      │  MODULE  │       │
│  │        │   │        │      │        │      │          │       │
│  │•Vector │   │•Ollama │      │•Schema │      │•SQL Val  │       │
│  │ Store  │   │ Client │      │ Loader │      │•Input    │       │
│  │•Embed  │   │•Prompt │      │•Query  │      │ Sanitize │       │
│  │•Retrieve   │ Builder│      │ Exec   │      │•Security │       │
│  └────┬───┘   └────┬───┘      └────┬───┘      └──────────┘       │
│       │            │               │                               │
└───────┼────────────┼───────────────┼───────────────────────────────┘
        │            │               │
        ▼            ▼               ▼
┌───────────┐  ┌──────────┐  ┌────────────┐
│ ChromaDB  │  │  Ollama  │  │ SQL Server │
│ (Embedded)│  │  (Local) │  │ (External) │
└───────────┘  └──────────┘  └────────────┘
```

**Legend**:
- **Boxes**: System components/modules
- **Arrows**: Data/control flow
- **Dashed lines**: Optional/future integrations
- **External systems**: Outside application boundary

---

### **3.2 Detailed Component Architecture**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION LAYERS                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    PRESENTATION LAYER                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │   │
│  │  │ Query Input  │  │   Results    │  │   History    │         │   │
│  │  │  Component   │  │   Display    │  │   Sidebar    │         │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │   │
│  │         │                 │                 │                   │   │
│  │         └─────────────────┼─────────────────┘                   │   │
│  │                           │                                     │   │
│  │                    ┌──────▼───────┐                             │   │
│  │                    │  Streamlit   │                             │   │
│  │                    │   Session    │                             │   │
│  │                    │  Management  │                             │   │
│  │                    └──────┬───────┘                             │   │
│  └───────────────────────────┼─────────────────────────────────────┘   │
│                               │                                         │
├───────────────────────────────┼─────────────────────────────────────────┤
│                               │                                         │
│  ┌────────────────────────────▼────────────────────────────────────┐   │
│  │                    APPLICATION LAYER                            │   │
│  │                                                                  │   │
│  │    ┌──────────────────────────────────────────────────────┐    │   │
│  │    │         QUERY PROCESSING PIPELINE                    │    │   │
│  │    │                                                       │    │   │
│  │    │  1. INPUT        2. INTENT       3. CONTEXT          │    │   │
│  │    │  Validation   → Classification → Retrieval           │    │   │
│  │    │                                                       │    │   │
│  │    │  4. SQL          5. VALIDATION   6. EXECUTION        │    │   │
│  │    │  Generation   → Safety Check  → DB Query            │    │   │
│  │    │                                                       │    │   │
│  │    │  7. FORMATTING   8. CACHING     9. LOGGING           │    │   │
│  │    │  Results      → Store Result → Audit Log            │    │   │
│  │    └───┬──────────────┬──────────────┬───────────────┘    │   │
│  │        │              │              │                    │   │
│  │        ▼              ▼              ▼                    │   │
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐              │   │
│  │  │ Convers.│    │ Query   │    │ Session │              │   │
│  │  │ Manager │    │Optimizer│    │ Store   │              │   │
│  │  └─────────┘    └─────────┘    └─────────┘              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                               │                                         │
├───────────────────────────────┼─────────────────────────────────────────┤
│                               │                                         │
│  ┌────────────────────────────▼────────────────────────────────────┐   │
│  │                    DOMAIN LAYER                                 │   │
│  │                                                                  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │   │
│  │  │    RAG      │  │     LLM     │  │  DATABASE   │            │   │
│  │  │   Engine    │  │   Engine    │  │   Engine    │            │   │
│  │  │             │  │             │  │             │            │   │
│  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │            │   │
│  │  │ │Embedding│ │  │ │ Prompt  │ │  │ │ Schema  │ │            │   │
│  │  │ │Generator│ │  │ │ Builder │ │  │ │ Loader  │ │            │   │
│  │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │            │   │
│  │  │             │  │             │  │             │            │   │
│  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │            │   │
│  │  │ │ Vector  │ │  │ │  Ollama │ │  │ │  Query  │ │            │   │
│  │  │ │ Search  │ │  │ │ Client  │ │  │ │Executor │ │            │   │
│  │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │            │   │
│  │  │             │  │             │  │             │            │   │
│  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │            │   │
│  │  │ │Context  │ │  │ │   SQL   │ │  │ │  Result │ │            │   │
│  │  │ │Ranker   │ │  │ │ Parser  │ │  │ │Formatter│ │            │   │
│  │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │            │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘            │   │
│  │                                                                  │   │
│  │  ┌──────────────────────────────────────────────────────────┐  │   │
│  │  │              VALIDATION ENGINE                           │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │   │
│  │  │  │  Input   │ │   SQL    │ │  Schema  │ │ Security │   │  │   │
│  │  │  │Validator │ │Validator │ │Validator │ │  Rules   │   │  │   │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │  │   │
│  │  └──────────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                               │                                         │
├───────────────────────────────┼─────────────────────────────────────────┤
│                               │                                         │
│  ┌────────────────────────────▼────────────────────────────────────┐   │
│  │                    INFRASTRUCTURE LAYER                         │   │
│  │                                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│  │  │  Logging │  │  Metrics │  │  Caching │  │   Config │       │   │
│  │  │  Service │  │  Service │  │  Service │  │  Manager │       │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │   │
│  │                                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│  │  │Connection│  │   File   │  │  Error   │  │   Event  │       │   │
│  │  │   Pool   │  │  Storage │  │  Handler │  │    Bus   │       │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### **3.3 Data Flow Diagram (Query Execution)**

```
┌──────┐
│ User │
└───┬──┘
    │ 1. Enter Query
    │    "How many patients admitted yesterday?"
    ▼
┌─────────────────────────────────────────────────────────┐
│                 UI LAYER (Streamlit)                    │
│  • Capture input                                        │
│  • Validate format (not empty, <500 chars)             │
│  • Show loading state                                   │
└────────────────────┬────────────────────────────────────┘
                     │ 2. Submit Query
                     ▼
┌─────────────────────────────────────────────────────────┐
│         CORE: Query Processor (Orchestrator)            │
│  • Create request context                               │
│  • Start transaction log                                │
│  • Initialize pipeline                                  │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │ 3. Classify Intent       │
        ▼                          ▼
┌─────────────────┐      ┌─────────────────┐
│ Intent          │      │ Conversation    │
│ Classifier      │      │ Manager         │
│ • Parse NL      │      │ • Check context │
│ • Detect type   │      │ • Resolve refs  │
│ • Extract       │      │ • Maintain      │
│   entities      │      │   history       │
└────────┬────────┘      └────────┬────────┘
         │                        │
         │ 4. Intent: COUNT       │
         │    Entities: patients, │
         │    Date: yesterday     │
         │                        │
         └────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│            RAG: Context Retrieval                       │
│  5. Generate Query Embedding                            │
│     "How many patients admitted yesterday?"             │
│                    ↓                                    │
│     Embedding: [0.23, -0.41, 0.15, ...]               │
│                    ↓                                    │
│  6. Search Vector Store (ChromaDB)                     │
│     • Semantic search for similar schemas               │
│     • Retrieve: "patient_master", "encounters"         │
│     • Retrieve: Example COUNT queries                   │
│     • Retrieve: Business rules (admit_date field)      │
│                    ↓                                    │
│  7. Rank & Filter Results                              │
│     Top 3 contexts:                                     │
│     - encounters table (relevance: 0.92)               │
│     - admit_date column (relevance: 0.89)              │
│     - Example: "SELECT COUNT(*) FROM..." (0.85)        │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ 8. Context Package
                     ▼
┌─────────────────────────────────────────────────────────┐
│              LLM: SQL Generation                        │
│  9. Build Prompt                                        │
│     ┌──────────────────────────────────────────────┐   │
│     │ You are SQL expert. Generate T-SQL query.   │   │
│     │                                               │   │
│     │ Schema:                                       │   │
│     │ - Table: encounters                           │   │
│     │   - patient_id (INT)                          │   │
│     │   - admit_date (DATE)                         │   │
│     │                                               │   │
│     │ Example:                                      │   │
│     │ Q: "How many patients yesterday?"             │   │
│     │ SQL: SELECT COUNT(*) FROM encounters         │   │
│     │      WHERE admit_date = DATEADD(day,-1,...)  │   │
│     │                                               │   │
│     │ User Question: "How many patients admitted   │   │
│     │ yesterday?"                                   │   │
│     │                                               │   │
│     │ Generate SQL:                                 │   │
│     └──────────────────────────────────────────────┘   │
│                    ↓                                    │
│  10. Send to Ollama                                    │
│      Model: sqlcoder:7b-q4                             │
│      Temperature: 0.1                                   │
│      Max tokens: 512                                    │
│                    ↓                                    │
│  11. Parse Response                                    │
│      Raw: "```sql\nSELECT COUNT(*)..."                │
│      Extracted: "SELECT COUNT(*) FROM encounters..."   │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ 12. Generated SQL
                     ▼
┌─────────────────────────────────────────────────────────┐
│           VALIDATION: Safety Checks                     │
│  13. Multi-Layer Validation                             │
│                                                         │
│  Layer 1: SQL Injection Check                          │
│  ✓ No suspicious patterns detected                     │
│                                                         │
│  Layer 2: Operation Type Check                         │
│  ✓ SELECT only (no DROP/DELETE/UPDATE)                │
│                                                         │
│  Layer 3: Schema Validation                            │
│  ✓ Table "encounters" exists                           │
│  ✓ Column "admit_date" exists                          │
│                                                         │
│  Layer 4: Complexity Check                             │
│  ✓ Simple query (no subqueries, 0 JOINs)              │
│                                                         │
│  Layer 5: Result Size Estimation                       │
│  ✓ COUNT query (returns 1 row)                        │
│                                                         │
│  VALIDATION: PASS ✓                                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ 14. Validated SQL
                     ▼
┌─────────────────────────────────────────────────────────┐
│           DATABASE: Query Execution                     │
│  15. Acquire Connection from Pool                      │
│      Connection ID: conn_12345                          │
│                    ↓                                    │
│  16. Execute SQL with Timeout (30s)                    │
│      SQL: SELECT COUNT(*) as patient_count             │
│           FROM encounters                               │
│           WHERE admit_date = DATEADD(day, -1,          │
│                 CAST(GETDATE() AS DATE))               │
│                    ↓                                    │
│  17. Fetch Results                                     │
│      Row 1: patient_count = 147                        │
│      Execution time: 0.8 seconds                        │
│                    ↓                                    │
│  18. Release Connection                                │
│      Connection returned to pool                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ 19. Raw Results
                     ▼
┌─────────────────────────────────────────────────────────┐
│         CORE: Result Formatting                         │
│  20. Format Response                                    │
│      • Natural language: "147 patients admitted         │
│        yesterday"                                       │
│      • Data table: [{"patient_count": 147}]            │
│      • Metadata: execution_time=0.8s, rows=1           │
│                    ↓                                    │
│  21. Cache Result (5 min TTL)                          │
│      Key: hash(query) → Result                         │
│                    ↓                                    │
│  22. Log Transaction                                   │
│      User: sarah_jones                                  │
│      Query: "How many patients..."                      │
│      SQL: "SELECT COUNT(*)..."                         │
│      Success: true                                      │
│      Duration: 3.2s (total)                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ 23. Formatted Response
                     ▼
┌─────────────────────────────────────────────────────────┐
│              UI: Display Results                        │
│  24. Render Components                                  │
│      ┌─────────────────────────────────────────────┐   │
│      │ ✓ Query executed successfully               │   │
│      │ Execution time: 0.8s | 1 row returned       │   │
│      │                                              │   │
│      │ ▼ Generated SQL (click to expand)           │   │
│      │                                              │   │
│      │ Answer: 147 patients admitted yesterday     │   │
│      │                                              │   │
│      │ ┌──────────────────┐                        │   │
│      │ │ patient_count    │                        │   │
│      │ ├──────────────────┤                        │   │
│      │ │ 147              │                        │   │
│      │ └──────────────────┘                        │   │
│      │                                              │   │
│      │ [Export CSV] [Export Excel] [Copy]          │   │
│      └─────────────────────────────────────────────┘   │
│                                                         │
│  25. Update History Sidebar                            │
│      Add to top of history list                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
                ┌────────┐
                │  User  │
                │ Sees   │
                │Results │
                └────────┘

Total Time: 3.2 seconds
├─ RAG Retrieval: 0.4s
├─ LLM Generation: 2.0s
├─ Validation: 0.05s
├─ DB Execution: 0.8s
└─ Formatting: 0.1s
(some parallel execution)
```

---

## **4. Technology Stack**

### **4.1 Technology Decision Matrix**

**Evaluation Criteria** (1-10 scale):
- **Performance**: Speed, efficiency, resource usage
- **Scalability**: Handles growth in users/data
- **Community**: Documentation, support, ecosystem
- **Learning Curve**: Team expertise required
- **Maintenance**: Long-term support, updates
- **Cost**: Licensing, infrastructure, operational
- **Compatibility**: Works with other stack components
- **Security**: Built-in security features

---

#### **Layer 1: Programming Language**

| Language | Performance | Scalability | Community | Learning | Maintenance | Cost | Compat | Security | **Total** | **Choice** |
|----------|-------------|-------------|-----------|----------|-------------|------|--------|----------|-----------|------------|
| **Python** | 7 | 8 | 10 | 9 | 9 | 10 | 10 | 8 | **8.88** | ✅ |
| JavaScript | 8 | 9 | 10 | 8 | 8 | 10 | 9 | 7 | 8.63 | |
| Java | 9 | 10 | 9 | 6 | 8 | 10 | 8 | 9 | 8.63 | |
| Go | 10 | 10 | 7 | 7 | 7 | 10 | 7 | 8 | 8.25 | |

**Winner**: Python 3.9+

**Rationale**:
- ✅ **ML/AI Ecosystem**: LangChain, ChromaDB, all ML libraries Python-native
- ✅ **Team Expertise**: Healthcare IT teams familiar with Python
- ✅ **Rapid Development**: High-level language accelerates MVP
- ✅ **Data Processing**: Pandas, NumPy excellent for query result manipulation
- ⚠️ **Performance**: CPU-bound; mitigated by Ollama handling heavy lifting

---

#### **Layer 2: Web Framework**

| Framework | Performance | Scalability | Community | Learning | Maintenance | Cost | Compat | Security | **Total** | **Choice** |
|-----------|-------------|-------------|-----------|----------|-------------|------|--------|----------|-----------|------------|
| **Streamlit** | 7 | 7 | 9 | 10 | 8 | 10 | 9 | 8 | **8.50** | ✅ MVP |
| FastAPI | 9 | 9 | 9 | 8 | 9 | 10 | 10 | 9 | 9.13 | Future |
| Flask | 8 | 8 | 10 | 9 | 9 | 10 | 10 | 7 | 8.88 | |
| Django | 7 | 9 | 10 | 7 | 10 | 10 | 9 | 10 | 9.00 | |

**Winner**: Streamlit (MVP), FastAPI (Production)

**Rationale - Streamlit**:
- ✅ **Development Speed**: Build UI in hours, not weeks
- ✅ **Python-Native**: No HTML/CSS/JS required
- ✅ **Session Management**: Built-in state management
- ✅ **Components**: Rich widget library for data apps
- ⚠️ **Scalability**: Limited to ~100 concurrent users

**Future Migration Path**: FastAPI for production scale
- Higher performance (async support)
- Better API design (REST, GraphQL)
- More scalable (ASGI vs WSGI)
- **Abstraction Layer**: Business logic separate from UI enables swap

---

#### **Layer 3: LLM Runtime**

| Runtime | Performance | Scalability | Community | Learning | Maintenance | Cost | Compat | Security | **Total** | **Choice** |
|---------|-------------|-------------|-----------|----------|-------------|------|--------|----------|-----------|------------|
| **Ollama** | 9 | 8 | 9 | 10 | 9 | 10 | 9 | 9 | **9.13** | ✅ |
| llama.cpp | 10 | 8 | 8 | 7 | 7 | 10 | 8 | 9 | 8.38 | Backup |
| vLLM | 10 | 9 | 7 | 6 | 7 | 10 | 7 | 8 | 8.00 | |
| HuggingFace | 7 | 9 | 10 | 8 | 9 | 10 | 10 | 8 | 8.88 | |

**Winner**: Ollama

**Rationale**:
- ✅ **Ease of Use**: `ollama pull model` → ready
- ✅ **Model Management**: Built-in model registry
- ✅ **Performance**: Optimized inference (quantization, batching)
- ✅ **API**: Simple REST API, Python SDK
- ✅ **Multi-Model**: Easy to switch models
- ✅ **Active Development**: Frequent updates, community

**Model Selection**: SQLCoder-7B-Q4
- Specialized for SQL generation
- 7B params = good balance (accuracy vs speed)
- Q4 quantization = 4GB RAM (fits hardware)

---

#### **Layer 4: Vector Database**

| Database | Performance | Scalability | Community | Learning | Maintenance | Cost | Compat | Security | **Total** | **Choice** |
|----------|-------------|-------------|-----------|----------|-------------|------|--------|----------|-----------|------------|
| **ChromaDB** | 8 | 7 | 8 | 10 | 8 | 10 | 9 | 8 | **8.50** | ✅ |
| FAISS | 10 | 8 | 9 | 7 | 7 | 10 | 8 | 7 | 8.25 | |
| Weaviate | 9 | 10 | 7 | 6 | 8 | 9 | 7 | 9 | 8.13 | |
| Qdrant | 9 | 9 | 7 | 7 | 7 | 10 | 7 | 8 | 8.00 | |

**Winner**: ChromaDB

**Rationale**:
- ✅ **Embedded**: Runs in-process (no separate server)
- ✅ **Simple**: Minimal configuration
- ✅ **Python-Native**: Clean Python API
- ✅ **Persistence**: Built-in disk persistence
- ✅ **Metadata Filtering**: Schema filtering capabilities
- ⚠️ **Scale**: Limited to ~1M documents (adequate for schema)

**Configuration**:
```python
import chromadb

client = chromadb.PersistentClient(path="./data/vector_db")
collection = client.get_or_create_collection(
    name="sql_schema",
    embedding_function=embedding_function,
    metadata={"hnsw:space": "cosine"}  # Similarity metric
)
```

---

#### **Layer 5: Database Connector**

| Library | Performance | Scalability | Community | Learning | Maintenance | Cost | Compat | Security | **Total** | **Choice** |
|---------|-------------|-------------|-----------|----------|-------------|------|--------|----------|-----------|------------|
| **pyodbc** | 9 | 9 | 9 | 8 | 9 | 10 | 10 | 9 | **9.13** | ✅ |
| pymssql | 8 | 8 | 7 | 8 | 7 | 10 | 9 | 8 | 8.13 | |
| SQLAlchemy | 8 | 9 | 10 | 7 | 10 | 10 | 10 | 9 | 9.13 | Future |

**Winner**: pyodbc (direct), SQLAlchemy (ORM layer)

**Rationale - pyodbc**:
- ✅ **Performance**: Direct ODBC, minimal overhead
- ✅ **Compatibility**: Works with SQL Server, PostgreSQL, MySQL
- ✅ **Mature**: Industry standard for Python SQL Server
- ✅ **Connection Pooling**: Supports pooling via external libs

**SQLAlchemy Layer**:
- Abstraction for multi-database support
- ORM not needed (raw SQL queries)
- Connection pooling built-in
- Used for schema introspection

---

#### **Layer 6: Embedding Model**

| Model | Performance | Scalability | Community | Learning | Maintenance | Cost | Compat | Security | **Total** | **Choice** |
|-------|-------------|-------------|-----------|----------|-------------|------|--------|----------|-----------|------------|
| **all-MiniLM-L6-v2** | 9 | 9 | 9 | 10 | 9 | 10 | 10 | 9 | **9.38** | ✅ |
| all-mpnet-base-v2 | 8 | 8 | 9 | 10 | 9 | 10 | 10 | 9 | 9.13 | |
| text-embedding-ada-002 | 10 | 10 | 8 | 9 | 9 | 6 | 7 | 7 | 8.25 | ❌ External |

**Winner**: all-MiniLM-L6-v2 (via sentence-transformers)

**Rationale**:
- ✅ **Performance**: 384-dim vectors, fast encoding (~5ms/query)
- ✅ **Local**: No external API (privacy requirement)
- ✅ **Quality**: Excellent semantic search quality
- ✅ **Size**: 80MB model (easy to deploy)
- ✅ **Community**: Most popular sentence-transformer model

---

### **4.2 Complete Technology Stack**

```
┌─────────────────────────────────────────────────────────┐
│                   PRESENTATION TIER                     │
├─────────────────────────────────────────────────────────┤
│ • Framework: Streamlit 1.28+                            │
│ • UI Components: Custom Streamlit components            │
│ • Styling: CSS (minimal custom styling)                 │
│ • State Management: Streamlit Session State             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   APPLICATION TIER                      │
├─────────────────────────────────────────────────────────┤
│ • Language: Python 3.9-3.11                             │
│ • Framework: Custom (Modular Monolith)                  │
│ • Orchestration: LangChain 0.1+                         │
│ • Async: asyncio (for future improvements)              │
│ • Configuration: PyYAML, python-dotenv                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   INTEGRATION TIER                      │
├─────────────────────────────────────────────────────────┤
│ LLM:                                                     │
│ • Runtime: Ollama 0.1+                                  │
│ • Model: SQLCoder-7B-Q4                                 │
│ • Client: ollama-python SDK                             │
│                                                         │
│ RAG:                                                     │
│ • Vector DB: ChromaDB 0.4+                              │
│ • Embeddings: sentence-transformers (all-MiniLM-L6-v2) │
│ • Retrieval: LangChain Retrievers                       │
│                                                         │
│ Database:                                                │
│ • Connector: pyodbc 5.0+                                │
│ • ORM Layer: SQLAlchemy 2.0+ (schema introspection)    │
│ • Pooling: SQLAlchemy Connection Pool                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE TIER                   │
├─────────────────────────────────────────────────────────┤
│ • Logging: Python logging + structlog                   │
│ • Metrics: Prometheus client                            │
│ • Caching: functools.lru_cache + Redis (optional)      │
│ • Configuration: YAML + Environment Variables           │
│ • Process Management: systemd / PM2                     │
│ • Containerization: Docker + Docker Compose             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   PERSISTENCE TIER                      │
├─────────────────────────────────────────────────────────┤
│ • Vector Store: ChromaDB (embedded, persistent)         │
│ • Schema Cache: JSON files (./data/schemas/)            │
│ • Query History: SQLite (./data/query_history.db)      │
│ • Application Logs: File system (./data/logs/)          │
│ • User Data: Streamlit Session State (memory)           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   EXTERNAL SYSTEMS                      │
├─────────────────────────────────────────────────────────┤
│ • SQL Server: 2016+ (read-only user)                    │
│ • SSO Provider: SAML/OAuth2 (Azure AD, Okta)           │
│ • Monitoring: Grafana + Prometheus (optional)           │
│ • Log Aggregation: ELK Stack / Splunk (optional)       │
└─────────────────────────────────────────────────────────┘
```

---

### **4.3 Key Dependencies**

**Production Dependencies** (`requirements.txt`):
```
# Core Framework
streamlit>=1.28.0
python-dotenv>=1.0.0

# LLM Integration
ollama>=0.1.0
langchain>=0.1.0
langchain-community>=0.0.10

# RAG Components
chromadb>=0.4.0
sentence-transformers>=2.2.0

# Database
pyodbc>=5.0.0
sqlalchemy>=2.0.0
pandas>=2.0.0

# Configuration & Utilities
pyyaml>=6.0
pydantic>=2.0.0  # Data validation
tenacity>=8.2.0  # Retry logic

# Logging & Monitoring
structlog>=23.1.0
prometheus-client>=0.17.0

# Security
cryptography>=41.0.0
```

---

## **5. Data Models and Schemas**

### **5.1 Core Domain Models**

```python
# src/core/models.py

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

# ================== QUERY MODELS ==================

class QueryIntent(Enum):
    """Types of query intents"""
    SELECT = "select"
    COUNT = "count"
    AGGREGATE = "aggregate"
    JOIN = "join"
    TIME_SERIES = "time_series"
    UNKNOWN = "unknown"


@dataclass
class UserQuery:
    """Represents a user's natural language query"""
    query_id: str
    user_id: str
    session_id: str
    text: str
    timestamp: datetime
    intent: Optional[QueryIntent] = None
    confidence: float = 0.0
    entities: Dict[str, Any] = None  # Extracted entities (dates, tables, etc.)
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = {}


@dataclass
class GeneratedSQL:
    """Represents generated SQL query"""
    sql_text: str
    dialect: str  # 'tsql', 'postgres', 'mysql'
    complexity: str  # 'simple', 'moderate', 'complex'
    tables_referenced: List[str]
    estimated_rows: Optional[int] = None
    generation_time_ms: float = 0.0
    confidence: float = 0.0


@dataclass
class QueryResult:
    """Represents query execution result"""
    query_id: str
    success: bool
    rows: List[Dict[str, Any]]
    row_count: int
    columns: List[str]
    execution_time_ms: float
    error_message: Optional[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


@dataclass
class QueryResponse:
    """Complete response to user query"""
    query_id: str
    original_query: str
    generated_sql: GeneratedSQL
    result: QueryResult
    natural_language_answer: str
    total_time_ms: float
    cached: bool = False


# ================== SCHEMA MODELS ==================

@dataclass
class ColumnDefinition:
    """Database column metadata"""
    name: str
    data_type: str  # 'INT', 'VARCHAR', 'DATE', etc.
    nullable: bool
    primary_key: bool = False
    foreign_key: Optional[str] = None  # "table.column"
    default_value: Optional[Any] = None
    description: Optional[str] = None
    sample_values: List[Any] = None
    
    def __post_init__(self):
        if self.sample_values is None:
            self.sample_values = []


@dataclass
class TableDefinition:
    """Database table metadata"""
    schema_name: str  # 'dbo', 'reporting', etc.
    table_name: str
    columns: List[ColumnDefinition]
    row_count: Optional[int] = None
    description: Optional[str] = None
    last_updated: Optional[datetime] = None
    indexes: List[str] = None
    
    def __post_init__(self):
        if self.indexes is None:
            self.indexes = []
    
    @property
    def full_name(self) -> str:
        return f"{self.schema_name}.{self.table_name}"


@dataclass
class Relationship:
    """Table relationship (foreign key)"""
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    relationship_type: str  # 'one-to-one', 'one-to-many', 'many-to-many'


@dataclass
class DatabaseSchema:
    """Complete database schema"""
    database_name: str
    tables: List[TableDefinition]
    relationships: List[Relationship]
    version: str
    last_refreshed: datetime


# ================== RAG MODELS ==================

@dataclass
class SchemaElement:
    """Single schema element for RAG"""
    element_id: str
    element_type: str  # 'table', 'column', 'relationship', 'business_rule'
    content: str  # Text description
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RetrievalContext:
    """Context retrieved from RAG"""
    query: str
    retrieved_elements: List[SchemaElement]
    retrieval_time_ms: float
    total_tokens: int


@dataclass
class ExampleQuery:
    """Example query pair for few-shot learning"""
    example_id: str
    natural_language: str
    sql_query: str
    tags: List[str]
    success_count: int = 0
    last_used: Optional[datetime] = None


# ================== VALIDATION MODELS ==================

class ValidationLevel(Enum):
    """Severity of validation issue"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Single validation issue"""
    level: ValidationLevel
    message: str
    rule: str  # Which validation rule triggered
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of validation checks"""
    passed: bool
    issues: List[ValidationIssue]
    validated_sql: Optional[str] = None  # Modified SQL if corrections made
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []
    
    def has_errors(self) -> bool:
        return any(issue.level in [ValidationLevel.ERROR, ValidationLevel.CRITICAL] 
                   for issue in self.issues)


# ================== SESSION MODELS ==================

@dataclass
class ConversationTurn:
    """Single turn in conversation"""
    turn_id: str
    user_query: UserQuery
    response: QueryResponse
    timestamp: datetime


@dataclass
class UserSession:
    """User session state"""
    session_id: str
    user_id: str
    started_at: datetime
    last_activity: datetime
    conversation_history: List[ConversationTurn]
    context: Dict[str, Any]  # Session-specific context
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []
        if self.context is None:
            self.context = {}


# ================== CONFIGURATION MODELS ==================

@dataclass
class DatabaseConfig:
    """Database connection configuration"""
    host: str
    port: int
    database: str
    username: str
    password: str
    driver: str = "ODBC Driver 17 for SQL Server"
    timeout: int = 30
    pool_size: int = 10


@dataclass
class OllamaConfig:
    """Ollama LLM configuration"""
    base_url: str = "http://localhost:11434"
    model: str = "sqlcoder:7b-q4"
    temperature: float = 0.1
    max_tokens: int = 512
    timeout: int = 45


@dataclass
class RAGConfig:
    """RAG configuration"""
    vector_store_path: str
    collection_name: str = "sql_schema"
    embedding_model: str = "all-MiniLM-L6-v2"
    top_k: int = 5
    similarity_threshold: float = 0.7
```

---

### **5.2 Database Schemas**

#### **Application Database (SQLite for Query History)**

```sql
-- data/query_history.db

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT,
    role TEXT,  -- 'admin', 'analyst', 'viewer'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE queries (
    query_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    query_text TEXT NOT NULL,
    intent TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_queries_user ON queries(user_id, submitted_at DESC);
CREATE INDEX idx_queries_session ON queries(session_id, submitted_at DESC);

CREATE TABLE generated_sql (
    sql_id TEXT PRIMARY KEY,
    query_id TEXT NOT NULL,
    sql_text TEXT NOT NULL,
    dialect TEXT,
    complexity TEXT,
    tables_referenced TEXT,  -- JSON array
    generation_time_ms REAL,
    confidence REAL,
    FOREIGN KEY (query_id) REFERENCES queries(query_id)
);

CREATE TABLE query_results (
    result_id TEXT PRIMARY KEY,
    query_id TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    row_count INTEGER,
    execution_time_ms REAL,
    error_message TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (query_id) REFERENCES queries(query_id)
);

CREATE TABLE query_cache (
    cache_key TEXT PRIMARY KEY,  -- Hash of query + schema version
    query_text TEXT,
    sql_text TEXT,
    result_json TEXT,  -- JSON serialized result
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    hit_count INTEGER DEFAULT 0
);

CREATE INDEX idx_cache_expires ON query_cache(expires_at);

CREATE TABLE example_queries (
    example_id TEXT PRIMARY KEY,
    category TEXT,  -- 'operations', 'financial', 'quality'
    natural_language TEXT NOT NULL,
    sql_query TEXT NOT NULL,
    tags TEXT,  -- JSON array
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_log (
    log_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    action TEXT NOT NULL,  -- 'query', 'export', 'admin_action'
    details TEXT,  -- JSON with action details
    ip_address TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_audit_user ON audit_log(user_id, timestamp DESC);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp DESC);
```

---

#### **Vector Store Schema (ChromaDB)**

```python
# ChromaDB Collection Structure

{
    "collection_name": "sql_schema",
    "metadata": {
        "hnsw:space": "cosine",
        "description": "Database schema elements for RAG"
    },
    "documents": [
        {
            "id": "table_encounters_001",
            "document": "Table: encounters. Contains patient encounter records...",
            "metadata": {
                "type": "table",
                "schema": "dbo",
                "table_name": "encounters",
                "row_count": 2500000,
                "last_updated": "2025-10-29T00:15:00Z"
            },
            "embedding": [0.23, -0.41, 0.15, ...]  # 384-dim vector
        },
        {
            "id": "column_encounters_admit_date_002",
            "document": "Column: encounters.admit_date (DATE). Date patient admitted...",
            "metadata": {
                "type": "column",
                "table": "encounters",
                "column_name": "admit_date",
                "data_type": "DATE",
                "nullable": false
            },
            "embedding": [0.19, -0.38, 0.22, ...]
        },
        {
            "id": "relationship_encounters_patients_003",
            "document": "Relationship: encounters.patient_id -> patients.patient_id...",
            "metadata": {
                "type": "relationship",
                "from_table": "encounters",
                "to_table": "patients",
                "relationship_type": "many-to-one"
            },
            "embedding": [0.31, -0.29, 0.18, ...]
        },
        {
            "id": "example_query_discharge_count_004",
            "document": "Q: How many patients discharged yesterday? SQL: SELECT COUNT(*)...",
            "metadata": {
                "type": "example",
                "category": "operations",
                "tags": ["discharge", "count", "date"],
                "success_rate": 0.95
            },
            "embedding": [0.27, -0.42, 0.13, ...]
        }
    ]
}
```

---

### **5.3 Data Flow Patterns**

#### **Pattern 1: Schema Ingestion Flow**

```
SQL Server Database
        │
        │ 1. Query INFORMATION_SCHEMA
        ▼
┌────────────────────────┐
│ Schema Loader Module   │
│ • Extract tables       │
│ • Extract columns      │
│ • Extract relationships│
└───────────┬────────────┘
            │ 2. Raw Schema Data
            ▼
┌────────────────────────┐
│ Schema Enricher        │
│ • Add descriptions     │
│ • Sample data values   │
│ • Calculate statistics │
└───────────┬────────────┘
            │ 3. Enriched Schema
            ▼
┌────────────────────────┐
│ Embedding Generator    │
│ • Create text descriptions
│ • Generate embeddings  │
│ • Batch processing     │
└───────────┬────────────┘
            │ 4. Schema + Embeddings
            ▼
┌────────────────────────┐
│ ChromaDB Indexer       │
│ • Store in vector DB   │
│ • Create indexes       │
│ • Update metadata      │
└───────────┬────────────┘
            │
            ▼
    [Vector Store Ready]
```

---

#### **Pattern 2: Query Result Caching**

```
User Query
    │
    ▼
┌─────────────────┐
│ Generate Cache  │
│ Key (MD5 Hash)  │
│ • Query text    │
│ • Schema version│
│ • User context  │
└────────┬────────┘
         │
         ▼
    [Check Cache]
         │
    ┌────┴────┐
    │         │
  Found    Not Found
    │         │
    ▼         ▼
[Return   [Execute
 Cached]   Pipeline]
    │         │
    │         ▼
    │    [Store in
    │     Cache]
    │         │
    └────┬────┘
         │
         ▼
    [Return to User]
```

---

## **6. Key Components Deep Dive**

### **6.1 Component: Query Processor (Orchestrator)**

**Responsibility**: Main orchestration engine coordinating all pipeline stages.

**Interfaces**:
```python
# src/core/query_processor.py

class QueryProcessor:
    """
    Central orchestrator for query processing pipeline.
    Coordinates: validation → RAG → LLM → validation → execution → formatting
    """
    
    def __init__(
        self,
        rag_engine: RAGEngine,
        llm_engine: LLMEngine,
        validator: QueryValidator,
        db_engine: DatabaseEngine,
        conversation_manager: ConversationManager
    ):
        self.rag = rag_engine
        self.llm = llm_engine
        self.validator = validator
        self.db = db_engine
        self.conversation = conversation_manager
        self.logger = get_logger(__name__)
        self.metrics = MetricsCollector()
    
    async def process_query(
        self,
        user_query: UserQuery,
        session: UserSession
    ) -> QueryResponse:
        """
        Process natural language query through complete pipeline.
        
        Pipeline Stages:
        1. Input validation
        2. Intent classification
        3. Context retrieval (RAG)
        4. SQL generation (LLM)
        5. SQL validation
        6. Query execution
        7. Result formatting
        8. Caching & logging
        
        Args:
            user_query: User's natural language query
            session: Current user session
            
        Returns:
            QueryResponse with SQL, results, and metadata
            
        Raises:
            ValidationError: If query fails safety checks
            LLMError: If SQL generation fails
            DatabaseError: If query execution fails
        """
        start_time = time.time()
        query_id = generate_uuid()
        
        try:
            # Stage 1: Input Validation
            self.logger.info(f"Processing query {query_id}", extra={"query": user_query.text})
            self.validator.validate_input(user_query.text)
            
            # Stage 2: Intent Classification
            intent = await self._classify_intent(user_query)
            user_query.intent = intent.type
            user_query.confidence = intent.confidence
            user_query.entities = intent.entities
            
            # Stage 3: Context Retrieval (RAG)
            context = await self.rag.retrieve_context(
                query=user_query.text,
                intent=intent,
                conversation_history=session.conversation_history
            )
            
            # Stage 4: SQL Generation (LLM)
            generated_sql = await self.llm.generate_sql(
                query=user_query,
                context=context,
                conversation=session.conversation_history[-5:]  # Last 5 turns
            )
            
            # Stage 5: SQL Validation
            validation_result = await self.validator.validate_sql(
                generated_sql.sql_text,
                context.retrieved_elements
            )
            
            if not validation_result.passed:
                if validation_result.has_errors():
                    raise ValidationError(validation_result.issues)
                # Has warnings but can proceed
                self.logger.warning(f"SQL validation warnings: {validation_result.issues}")
            
            # Stage 6: Query Execution
            result = await self.db.execute_query(
                sql=generated_sql.sql_text,
                timeout=30
            )
            
            # Stage 7: Result Formatting
            nl_answer = await self._generate_natural_language_answer(
                query=user_query,
                result=result
            )
            
            # Stage 8: Create Response
            response = QueryResponse(
                query_id=query_id,
                original_query=user_query.text,
                generated_sql=generated_sql,
                result=result,
                natural_language_answer=nl_answer,
                total_time_ms=(time.time() - start_time) * 1000
            )
            
            # Stage 9: Caching & Logging
            await self._cache_result(user_query, response)
            await self._log_query(user_query, response, session)
            
            # Stage 10: Update Conversation
            self.conversation.add_turn(session, user_query, response)
            
            # Collect metrics
            self.metrics.record_query_success(response.total_time_ms)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Query processing failed: {e}", exc_info=True)
            self.metrics.record_query_failure()
            raise
```

**Internal Methods**:
```python
    async def _classify_intent(self, query: UserQuery) -> Intent:
        """Classify query intent using simple heuristics + LLM"""
        # Heuristic classification
        if any(word in query.text.lower() for word in ['how many', 'count', 'number of']):
            intent_type = QueryIntent.COUNT
        elif any(word in query.text.lower() for word in ['average', 'sum', 'total', 'mean']):
            intent_type = QueryIntent.AGGREGATE
        else:
            intent_type = QueryIntent.SELECT
        
        # Extract entities (dates, table hints, etc.)
        entities = self._extract_entities(query.text)
        
        return Intent(type=intent_type, confidence=0.85, entities=entities)
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities like dates, numbers, table names"""
        entities = {}
        
        # Date extraction
        date_parser = DateParser()
        if date_info := date_parser.parse(text):
            entities['date'] = date_info
        
        # Number extraction
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            entities['numbers'] = [int(n) for n in numbers]
        
        return entities
    
    async def _generate_natural_language_answer(
        self,
        query: UserQuery,
        result: QueryResult
    ) -> str:
        """Generate natural language answer from results"""
        if not result.success:
            return f"Query failed: {result.error_message}"
        
        if result.row_count == 0:
            return "No results found for your query."
        
        # For COUNT queries, extract the count value
        if query.intent == QueryIntent.COUNT and result.row_count == 1:
            count_value = list(result.rows[0].values())[0]
            return f"{count_value} {self._pluralize('record', count_value)} found."
        
        # For other queries
        return f"{result.row_count} {self._pluralize('row', result.row_count)} returned."
    
    async def _cache_result(self, query: UserQuery, response: QueryResponse):
        """Cache query result for fast repeat access"""
        cache_key = self._generate_cache_key(query)
        cache_entry = {
            'query': query.text,
            'sql': response.generated_sql.sql_text,
            'result': response.result,
            'cached_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(minutes=5)
        }
        await self.cache.set(cache_key, cache_entry, ttl=300)  # 5 minutes
```

**Dependencies**:
- RAGEngine (context retrieval)
- LLMEngine (SQL generation)
- QueryValidator (safety checks)
- DatabaseEngine (query execution)
- ConversationManager (session state)

---

### **6.2 Component: RAG Engine**

**Responsibility**: Retrieve relevant context from vector store for SQL generation.

```python
# src/rag/rag_engine.py

class RAGEngine:
    """
    Retrieval-Augmented Generation engine.
    Retrieves relevant schema, examples, and business rules from vector store.
    """
    
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_generator: EmbeddingGenerator,
        config: RAGConfig
    ):
        self.vector_store = vector_store
        self.embeddings = embedding_generator
        self.config = config
        self.logger = get_logger(__name__)
    
    async def retrieve_context(
        self,
        query: str,
        intent: Intent,
        conversation_history: List[ConversationTurn]
    ) -> RetrievalContext:
        """
        Retrieve relevant context for query generation.
        
        Retrieval Strategy:
        1. Generate query embedding
        2. Search vector store (semantic similarity)
        3. Filter by metadata (table types, relevance)
        4. Rank results
        5. Limit to token budget
        
        Args:
            query: Natural language query
            intent: Classified query intent
            conversation_history: Recent conversation for context
            
        Returns:
            RetrievalContext with relevant schema elements
        """
        start_time = time.time()
        
        # 1. Generate Query Embedding
        query_embedding = await self.embeddings.generate(query)
        
        # 2. Semantic Search
        search_results = await self.vector_store.search(
            query_embedding=query_embedding,
            top_k=self.config.top_k * 2,  # Retrieve more, filter later
            filters={
                'type': ['table', 'column', 'relationship', 'example']
            }
        )
        
        # 3. Filter by Relevance Threshold
        filtered_results = [
            result for result in search_results
            if result.similarity_score >= self.config.similarity_threshold
        ]
        
        # 4. Categorize Results
        tables = [r for r in filtered_results if r.metadata['type'] == 'table']
        columns = [r for r in filtered_results if r.metadata['type'] == 'column']
        examples = [r for r in filtered_results if r.metadata['type'] == 'example']
        
        # 5. Rank by Relevance + Recency
        ranked_elements = self._rank_elements(
            tables=tables,
            columns=columns,
            examples=examples,
            intent=intent
        )
        
        # 6. Limit to Token Budget
        selected_elements = self._fit_to_token_budget(
            ranked_elements,
            max_tokens=self.config.max_context_tokens
        )
        
        retrieval_time = (time.time() - start_time) * 1000
        
        self.logger.info(
            f"Retrieved {len(selected_elements)} context elements",
            extra={'retrieval_time_ms': retrieval_time}
        )
        
        return RetrievalContext(
            query=query,
            retrieved_elements=selected_elements,
            retrieval_time_ms=retrieval_time,
            total_tokens=self._count_tokens(selected_elements)
        )
    
    def _rank_elements(
        self,
        tables: List[SearchResult],
        columns: List[SearchResult],
        examples: List[SearchResult],
        intent: Intent
    ) -> List[SchemaElement]:
        """
        Rank elements by relevance score + heuristics.
        
        Ranking factors:
        - Semantic similarity score (from vector search)
        - Element type priority (tables > columns > examples)
        - Recency (for examples)
        - Usage frequency (for popular tables/examples)
        """
        ranked = []
        
        # Tables: High priority (schema foundation)
        for table in tables[:3]:  # Top 3 tables
            ranked.append(SchemaElement(
                element_id=table.id,
                element_type='table',
                content=table.document,
                metadata=table.metadata,
                score=table.similarity_score * 1.2  # Boost table scores
            ))
        
        # Columns: Related to selected tables
        table_names = [r.metadata['table_name'] for r in tables[:3]]
        relevant_columns = [
            c for c in columns
            if c.metadata.get('table') in table_names
        ]
        for column in relevant_columns[:5]:  # Top 5 columns
            ranked.append(SchemaElement(
                element_id=column.id,
                element_type='column',
                content=column.document,
                metadata=column.metadata,
                score=column.similarity_score
            ))
        
        # Examples: Match intent type
        intent_matched_examples = [
            ex for ex in examples
            if intent.type.value in ex.metadata.get('tags', [])
        ]
        for example in intent_matched_examples[:2]:  # Top 2 examples
            ranked.append(SchemaElement(
                element_id=example.id,
                element_type='example',
                content=example.document,
                metadata=example.metadata,
                score=example.similarity_score * 1.1  # Boost examples
            ))
        
        # Sort by adjusted score
        ranked.sort(key=lambda x: x.score, reverse=True)
        return ranked
    
    def _fit_to_token_budget(
        self,
        elements: List[SchemaElement],
        max_tokens: int
    ) -> List[SchemaElement]:
        """Fit elements within token budget"""
        selected = []
        total_tokens = 0
        
        for element in elements:
            element_tokens = self._count_element_tokens(element)
            if total_tokens + element_tokens <= max_tokens:
                selected.append(element)
                total_tokens += element_tokens
            else:
                break  # Exceeded budget
        
        return selected
    
    def _count_element_tokens(self, element: SchemaElement) -> int:
        """Estimate token count for element (rough: 4 chars = 1 token)"""
        return len(element.content) // 4
```

---

### **6.3 Component: LLM Engine**

**Responsibility**: Generate SQL from natural language using Ollama LLM.

```python
# src/llm/llm_engine.py

class LLMEngine:
    """
    LLM integration for SQL generation.
    Manages prompt construction, Ollama communication, SQL parsing.
    """
    
    def __init__(
        self,
        ollama_client: OllamaClient,
        prompt_builder: PromptBuilder,
        config: OllamaConfig
    ):
        self.ollama = ollama_client
        self.prompt_builder = prompt_builder
        self.config = config
        self.logger = get_logger(__name__)
    
    async def generate_sql(
        self,
        query: UserQuery,
        context: RetrievalContext,
        conversation: List[ConversationTurn]
    ) -> GeneratedSQL:
        """
        Generate SQL from natural language query.
        
        Process:
        1. Build prompt with context
        2. Send to Ollama
        3. Parse SQL from response
        4. Extract metadata
        
        Args:
            query: User's natural language query
            context: Retrieved RAG context
            conversation: Recent conversation turns
            
        Returns:
            GeneratedSQL with query text and metadata
        """
        start_time = time.time()
        
        # 1. Build Prompt
        prompt = self.prompt_builder.build(
            query=query,
            context=context,
            conversation=conversation,
            dialect='tsql'
        )
        
        self.logger.debug(f"Generated prompt ({len(prompt)} chars)")
        
        # 2. Call Ollama
        try:
            response = await self.ollama.generate(
                model=self.config.model,
                prompt=prompt,
                options={
                    'temperature': self.config.temperature,
                    'top_p': 0.9,
                    'stop': [';', '```'],
                    'num_predict': self.config.max_tokens
                },
                timeout=self.config.timeout
            )
        except OllamaError as e:
            self.logger.error(f"Ollama generation failed: {e}")
            raise LLMError(f"SQL generation failed: {e}")
        
        # 3. Parse SQL
        sql_text = self._parse_sql_from_response(response['response'])
        
        # 4. Extract Metadata
        complexity = self._assess_complexity(sql_text)
        tables = self._extract_tables(sql_text)
        
        generation_time = (time.time() - start_time) * 1000
        
        return GeneratedSQL(
            sql_text=sql_text,
            dialect='tsql',
            complexity=complexity,
            tables_referenced=tables,
            generation_time_ms=generation_time,
            confidence=0.85  # Could implement confidence scoring
        )
    
    def _parse_sql_from_response(self, response_text: str) -> str:
        """Extract clean SQL from LLM response"""
        # Remove markdown code blocks
        sql = response_text
        sql = re.sub(r'```sql\n', '', sql)
        sql = re.sub(r'```\n?', '', sql)
        
        # Remove explanatory text (heuristic: SQL starts with SELECT/WITH)
        lines = sql.split('\n')
        sql_lines = []
        in_sql = False
        for line in lines:
            if re.match(r'^\s*(SELECT|WITH|INSERT|UPDATE|DELETE)', line, re.IGNORECASE):
                in_sql = True
            if in_sql:
                sql_lines.append(line)
        
        sql = '\n'.join(sql_lines).strip()
        
        # Remove trailing semicolon if present
        sql = sql.rstrip(';')
        
        return sql
    
    def _assess_complexity(self, sql: str) -> str:
        """Assess SQL query complexity"""
        sql_upper = sql.upper()
        
        # Count complexity indicators
        join_count = sql_upper.count('JOIN')
        subquery_count = sql_upper.count('SELECT') - 1  # Minus main SELECT
        cte_count = sql_upper.count('WITH')
        
        if cte_count > 0 or subquery_count > 2 or join_count > 5:
            return 'complex'
        elif join_count > 2 or subquery_count > 0:
            return 'moderate'
        else:
            return 'simple'
    
    def _extract_tables(self, sql: str) -> List[str]:
        """Extract table names from SQL"""
        # Simple regex-based extraction (could use SQL parser for accuracy)
        pattern = r'FROM\s+([a-zA-Z_][a-zA-Z0-9_.]*)|JOIN\s+([a-zA-Z_][a-zA-Z0-9_.]*)'
        matches = re.findall(pattern, sql, re.IGNORECASE)
        tables = [m[0] or m[1] for m in matches]
        return list(set(tables))  # Unique tables
```

---

### **6.4 Component: Query Validator**

**Responsibility**: Multi-layer validation to prevent harmful SQL execution.

```python
# src/validation/query_validator.py

class QueryValidator:
    """
    Multi-layer SQL validation for security and correctness.
    
    Validation Layers:
    1. SQL Injection prevention
    2. Prohibited operation blocking
    3. Schema validation
    4. Complexity limits
    5. Result size estimation
    """
    
    def __init__(self, schema_provider: SchemaProvider, config: ValidationConfig):
        self.schema = schema_provider
        self.config = config
        self.logger = get_logger(__name__)
    
    async def validate_sql(
        self,
        sql: str,
        context_elements: List[SchemaElement]
    ) -> ValidationResult:
        """
        Validate SQL query through all security layers.
        
        Args:
            sql: Generated SQL query
            context_elements: Schema elements used in generation
            
        Returns:
            ValidationResult with issues and corrected SQL
        """
        issues = []
        
        # Layer 1: SQL Injection Check
        injection_issues = self._check_sql_injection(sql)
        issues.extend(injection_issues)
        
        # Layer 2: Prohibited Operations
        operation_issues = self._check_prohibited_operations(sql)
        issues.extend(operation_issues)
        
        # Layer 3: Schema Validation
        schema_issues = await self._validate_schema_references(sql)
        issues.extend(schema_issues)
        
        # Layer 4: Complexity Check
        complexity_issues = self._check_complexity(sql)
        issues.extend(complexity_issues)
        
        # Layer 5: Result Size Estimation
        size_issues = self._estimate_result_size(sql)
        issues.extend(size_issues)
        
        # Determine if validation passed
        has_critical_errors = any(
            issue.level in [ValidationLevel.ERROR, ValidationLevel.CRITICAL]
            for issue in issues
        )
        
        return ValidationResult(
            passed=not has_critical_errors,
            issues=issues,
            validated_sql=sql
        )
    
    def _check_sql_injection(self, sql: str) -> List[ValidationIssue]:
        """Check for SQL injection patterns"""
        issues = []
        sql_upper = sql.upper()
        
        # Suspicious patterns
        injection_patterns = [
            (r';\s*(DROP|DELETE|UPDATE|INSERT)', 'Multi-statement injection'),
            (r'--', 'Comment injection'),
            (r'/\*.*\*/', 'Block comment injection'),
            (r'EXEC\s*\(', 'Dynamic SQL execution'),
            (r'xp_cmdshell', 'System command execution'),
            (r'sp_executesql', 'Dynamic SQL procedure')
        ]
        
        for pattern, description in injection_patterns:
            if re.search(pattern, sql_upper):
                issues.append(ValidationIssue(
                    level=ValidationLevel.CRITICAL,
                    message=f"Potential SQL injection detected: {description}",
                    rule='sql_injection_prevention'
                ))
        
        return issues
    
    def _check_prohibited_operations(self, sql: str) -> List[ValidationIssue]:
        """Block non-SELECT operations"""
        issues = []
        sql_upper = sql.upper().strip()
        
        prohibited_keywords = [
            'DROP', 'DELETE', 'UPDATE', 'INSERT', 'TRUNCATE',
            'ALTER', 'CREATE', 'GRANT', 'REVOKE', 'EXEC'
        ]
        
        # Check if query starts with prohibited keyword
        first_word = sql_upper.split()[0] if sql_upper else ''
        if first_word in prohibited_keywords:
            issues.append(ValidationIssue(
                level=ValidationLevel.CRITICAL,
                message=f"Prohibited operation: {first_word}. Only SELECT queries allowed.",
                rule='read_only_enforcement',
                suggestion="Rephrase query as a SELECT statement."
            ))
        
        return issues
    
    async def _validate_schema_references(self, sql: str) -> List[ValidationIssue]:
        """Validate that referenced tables/columns exist"""
        issues = []
        
        # Extract table references
        tables = self._extract_table_references(sql)
        
        for table in tables:
            if not await self.schema.table_exists(table):
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Table '{table}' does not exist in database.",
                    rule='schema_validation',
                    suggestion=f"Did you mean: {await self.schema.suggest_table(table)}"
                ))
        
        # Extract column references (more complex, simplified here)
        # Full implementation would parse SQL AST
        
        return issues
    
    def _check_complexity(self, sql: str) -> List[ValidationIssue]:
        """Check query complexity limits"""
        issues = []
        sql_upper = sql.upper()
        
        # Count JOINs
        join_count = sql_upper.count('JOIN')
        if join_count > self.config.max_joins:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message=f"Query has {join_count} JOINs (max recommended: {self.config.max_joins})",
                rule='complexity_limit',
                suggestion="Consider breaking into multiple simpler queries."
            ))
        
        # Check subquery nesting
        nesting_level = self._calculate_nesting_level(sql)
        if nesting_level > self.config.max_subquery_depth:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message=f"Subquery nesting depth {nesting_level} exceeds recommended {self.config.max_subquery_depth}",
                rule='complexity_limit'
            ))
        
        return issues
    
    def _estimate_result_size(self, sql: str) -> List[ValidationIssue]:
        """Estimate and warn about large result sets"""
        issues = []
        sql_upper = sql.upper()
        
        # Check for TOP/LIMIT clause
        has_limit = 'TOP' in sql_upper or 'LIMIT' in sql_upper
        
        # Check for WHERE clause
        has_where = 'WHERE' in sql_upper
        
        if not has_limit and not has_where:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message="Query may return large result set (no LIMIT or WHERE clause)",
                rule='result_size_estimation',
                suggestion="Add date filters or TOP clause to limit results."
            ))
        
        return issues
```

---

## **7. Scalability, Security, and Performance Architecture**

### **7.1 Scalability Strategy**

#### **Vertical Scaling (Phase 1)**

**Current Bottlenecks**:
1. **LLM Inference**: CPU-bound, 2-3s per query
2. **Database Queries**: I/O-bound, 0.5-2s per query
3. **Vector Search**: Memory-bound, <500ms per search

**Vertical Scaling Approach**:
```
Current: 16GB RAM, 8 cores
├─ LLM (Ollama): 8GB RAM, 4 cores
├─ Application: 4GB RAM, 2 cores
├─ ChromaDB: 2GB RAM, 1 core
└─ Overhead: 2GB RAM, 1 core

Scaled: 32GB RAM, 16 cores
├─ LLM (Ollama): 16GB RAM, 8 cores (run 2 instances)
├─ Application: 8GB RAM, 4 cores
├─ ChromaDB: 4GB RAM, 2 cores
└─ Overhead: 4GB RAM, 2 cores

Performance Gain: 2x concurrent capacity (20→40 users)
```

---

#### **Horizontal Scaling (Phase 2 - If Needed)**

**Architecture Evolution**:

```
┌──────────────────────────────────────────────────────┐
│            Load Balancer (HAProxy/Nginx)             │
└────────────┬────────────┬──────────────┬─────────────┘
             │            │              │
             ▼            ▼              ▼
      ┌───────────┐ ┌───────────┐ ┌───────────┐
      │Instance 1 │ │Instance 2 │ │Instance 3 │
      │ (App +    │ │ (App +    │ │ (App +    │
      │  Ollama)  │ │  Ollama)  │ │  Ollama)  │
      └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
            │             │             │
            └─────────────┼─────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ Shared Redis  │
                  │  (Sessions +  │
                  │   Cache)      │
                  └───────┬───────┘
                          │
           ┌──────────────┼──────────────┐
           │              │              │
           ▼              ▼              ▼
    ┌───────────┐  ┌───────────┐  ┌───────────┐
    │ ChromaDB  │  │SQL Server │  │PostgreSQL │
    │ (Shared)  │  │  (Read    │  │  (Query   │
    │           │  │  Replica) │  │  History) │
    └───────────┘  └───────────┘  └───────────┘
```

**Changes Required**:
- **Session Management**: Move from memory to Redis
- **Vector Store**: Shared ChromaDB or migrate to Weaviate cluster
- **Query Cache**: Redis instead of in-memory
- **Database**: Read replicas for query load
- **Sticky Sessions**: Route user to same instance for conversation continuity

---

#### **Component-Level Scaling**

**LLM Scaling**:
```python
# Load Balancing across multiple Ollama instances

class LoadBalancedLLMEngine:
    def __init__(self, ollama_endpoints: List[str]):
        self.clients = [OllamaClient(url) for url in ollama_endpoints]
        self.current_index = 0
        self.lock = asyncio.Lock()
    
    async def generate_sql(self, *args, **kwargs):
        async with self.lock:
            # Round-robin load balancing
            client = self.clients[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.clients)
        
        return await client.generate(*args, **kwargs)
```

**Database Connection Pooling**:
```python
# SQLAlchemy connection pool

engine = create_engine(
    connection_string,
    poolclass=QueuePool,
    pool_size=20,        # Connections maintained
    max_overflow=10,     # Additional connections when busy
    pool_timeout=30,     # Wait time for available connection
    pool_recycle=3600,   # Recycle connections hourly
    pool_pre_ping=True   # Test connection before use
)
```

---

### **7.2 Security Architecture**

#### **Defense-in-Depth Layers**

```
┌────────────────────────────────────────────────────────┐
│ Layer 1: Network Security                             │
│ • Firewall rules                                       │
│ • VPN access for remote users                          │
│ • TLS 1.3 for all connections                          │
└────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│ Layer 2: Authentication & Authorization                │
│ • SSO (SAML/OAuth2)                                    │
│ • MFA required                                         │
│ • RBAC (Role-Based Access Control)                     │
│ • Session timeout (4 hours)                            │
└────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│ Layer 3: Application Security                          │
│ • Input validation & sanitization                      │
│ • CSRF protection                                      │
│ • XSS prevention (Streamlit handles)                   │
│ • Security headers (CSP, HSTS, X-Frame-Options)        │
└────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│ Layer 4: Query Validation                              │
│ • SQL injection prevention                             │
│ • Prohibited operation blocking                        │
│ • Schema validation                                    │
│ • Complexity limits                                    │
└────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│ Layer 5: Database Security                             │
│ • Read-only database user                              │
│ • Row-level security (if supported)                    │
│ • Query timeout enforcement                            │
│ • Connection encryption (TLS)                          │
└────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│ Layer 6: Audit & Monitoring                            │
│ • Comprehensive audit logging                          │
│ • Security event monitoring                            │
│ • Anomaly detection                                    │
│ • Incident response procedures                         │
└────────────────────────────────────────────────────────┘
```

---

#### **HIPAA Compliance Mapping**

| **HIPAA Requirement** | **Architectural Implementation** |
|-----------------------|----------------------------------|
| **§164.308(a)(1)(ii)(D)** - Information System Activity Review | Comprehensive audit logging to `audit_log` table |
| **§164.308(a)(3)(i)** - Workforce Access Control | RBAC with user roles (admin/analyst/viewer) |
| **§164.308(a)(4)(i)** - Access Management | SSO integration, MFA enforcement |
| **§164.308(a)(5)(ii)(C)** - Log-in Monitoring | Failed login tracking, account lockout |
| **§164.310(d)(1)** - Device Controls | No PHI stored locally; vector store contains schema only |
| **§164.312(a)(1)** - Access Control | Role-based database permissions |
| **§164.312(a)(2)(i)** - Unique User ID | User ID in all log entries |
| **§164.312(b)** - Audit Controls | Immutable audit logs with cryptographic integrity |
| **§164.312(c)(1)** - Integrity Controls | Data validation prevents corruption |
| **§164.312(d)** - Person/Entity Authentication | SSO with MFA |
| **§164.312(e)(1)** - Transmission Security | TLS 1.3 for all network communication |

---

### **7.3 Performance Optimization**

#### **Caching Strategy**

**Multi-Level Cache**:

```
┌──────────────────────────────────────────────────────┐
│ L1: In-Memory Cache (functools.lru_cache)           │
│ • Schema metadata (30 min TTL)                       │
│ • Embedding model (persistent)                       │
│ • Configuration (persistent)                         │
│ Hit Rate Target: >80%                                │
└──────────────────────────────────────────────────────┘
                        │ Miss
                        ▼
┌──────────────────────────────────────────────────────┐
│ L2: Query Result Cache (Redis / SQLite)             │
│ • Query results (5 min TTL)                          │
│ • Frequently accessed schemas (1 hour TTL)           │
│ • Popular example queries (24 hour TTL)              │
│ Hit Rate Target: >50%                                │
└──────────────────────────────────────────────────────┘
                        │ Miss
                        ▼
┌──────────────────────────────────────────────────────┐
│ L3: Vector Store / Database                          │
│ • Full schema retrieval                              │
│ • Query execution                                    │
│ • Fresh data always                                  │
└──────────────────────────────────────────────────────┘
```

**Implementation**:
```python
from functools import lru_cache
import hashlib

class CachedQueryProcessor:
    def __init__(self, processor: QueryProcessor, cache_ttl: int = 300):
        self.processor = processor
        self.cache_ttl = cache_ttl
        self.cache = {}  # Or Redis client
    
    async def process_query(self, user_query: UserQuery, session: UserSession):
        # Generate cache key
        cache_key = self._generate_cache_key(user_query, session)
        
        # Check cache
        if cached_result := await self._get_from_cache(cache_key):
            cached_result.cached = True
            return cached_result
        
        # Process query (cache miss)
        result = await self.processor.process_query(user_query, session)
        
        # Store in cache
        await self._store_in_cache(cache_key, result, ttl=self.cache_ttl)
        
        return result
    
    def _generate_cache_key(self, query: UserQuery, session: UserSession) -> str:
        # Hash query text + schema version + user context
        key_components = [
            query.text.lower().strip(),
            self.processor.schema.version,
            session.context.get('database', 'default')
        ]
        key_string = '|'.join(key_components)
        return hashlib.md5(key_string.encode()).hexdigest()
```

---

#### **Database Query Optimization**

**Index Recommendations**:
```sql
-- SQL Server indexes for query history database

-- User query history lookup
CREATE INDEX idx_queries_user_time 
ON queries(user_id, submitted_at DESC);

-- Session queries lookup
CREATE INDEX idx_queries_session 
ON queries(session_id, submitted_at DESC);

-- Cache key lookup
CREATE INDEX idx_cache_key 
ON query_cache(cache_key);

-- Cache expiration cleanup
CREATE INDEX idx_cache_expires 
ON query_cache(expires_at) 
WHERE expires_at IS NOT NULL;

-- Audit log searches
CREATE INDEX idx_audit_timestamp 
ON audit_log(timestamp DESC);

CREATE INDEX idx_audit_user_action 
ON audit_log(user_id, action, timestamp DESC);
```

**Query Execution Optimization**:
```python
class OptimizedDatabaseEngine:
    async def execute_query(self, sql: str, timeout: int = 30):
        # Add query hints for performance
        optimized_sql = self._add_query_hints(sql)
        
        # Execute with timeout
        with self.connection_pool.get_connection() as conn:
            conn.execute(f"SET LOCK_TIMEOUT {timeout * 1000}")  # milliseconds
            conn.execute(f"SET QUERY_GOVERNOR_COST_LIMIT {timeout}")
            
            result = conn.execute(optimized_sql)
        
        return result
    
    def _add_query_hints(self, sql: str) -> str:
        # Add OPTION (MAXDOP 4) for parallel execution on multi-core
        if 'OPTION' not in sql.upper():
            sql += " OPTION (MAXDOP 4, RECOMPILE)"
        return sql
```

---

#### **LLM Inference Optimization**

**Prompt Optimization**:
```python
class OptimizedPromptBuilder:
    def build(self, query: UserQuery, context: RetrievalContext) -> str:
        # Minimize prompt tokens while maintaining quality
        
        # 1. Compress schema descriptions
        compressed_schema = self._compress_schema(context.retrieved_elements)
        
        # 2. Use concise examples
        concise_examples = self._select_minimal_examples(context, max_examples=2)
        
        # 3. Remove redundant instructions
        prompt = f"""Generate T-SQL for: "{query.text}"

Schema:
{compressed_schema}

Example:
{concise_examples}

SQL:"""
        
        return prompt
    
    def _compress_schema(self, elements: List[SchemaElement]) -> str:
        # Compact format: Table(col1 TYPE, col2 TYPE)
        schema_lines = []
        for element in elements:
            if element.element_type == 'table':
                columns = element.metadata.get('columns', [])
                col_str = ', '.join([f"{c['name']} {c['type']}" for c in columns[:5]])  # Top 5 columns
                schema_lines.append(f"{element.metadata['table_name']}({col_str})")
        return '\n'.join(schema_lines)
```

**Model Quantization**:
```bash
# Use quantized model for faster inference
ollama pull sqlcoder:7b-q4  # 4-bit quantization

# vs
ollama pull sqlcoder:7b     # Full precision (slower, more accurate)

# Performance comparison:
# Q4: ~2.0s inference, 4GB RAM, 85% accuracy
# FP16: ~3.5s inference, 8GB RAM, 87% accuracy

# Trade-off: 2% accuracy loss for 43% speed gain
```

---

## **8. Integration Points**

### **8.1 External System Integrations**

```
┌─────────────────────────────────────────────────────┐
│           SQL RAG Ollama Application                │
└──────────┬────────┬────────┬────────┬───────────────┘
           │        │        │        │
           ▼        ▼        ▼        ▼
    ┌──────────┐ ┌──────┐ ┌──────┐ ┌───────────┐
    │SQL Server│ │ SSO  │ │ SIEM │ │ Monitoring│
    │(Read-Only│ │(SAML)│ │(Logs)│ │(Metrics)  │
    └──────────┘ └──────┘ └──────┘ └───────────┘
```

---

#### **Integration 1: SQL Server Database**

**Connection Method**: ODBC via pyodbc

**Configuration**:
```yaml
# config/database.yaml
sql_server:
  host: ${DB_HOST}
  port: 1433
  database: ${DB_NAME}
  username: ${DB_USER}  # Read-only user
  password: ${DB_PASSWORD}
  driver: "ODBC Driver 17 for SQL Server"
  connection_string: >
    Driver={ODBC Driver 17 for SQL Server};
    Server=${DB_HOST},${DB_PORT};
    Database=${DB_NAME};
    UID=${DB_USER};
    PWD=${DB_PASSWORD};
    Encrypt=yes;
    TrustServerCertificate=no;
```

**Data Flow**:
1. Application requests schema metadata via INFORMATION_SCHEMA queries
2. User queries converted to SQL, executed with 30s timeout
3. Results returned as row dictionaries
4. Connection returned to pool after use

**Error Handling**:
- Connection failures: Retry 3 times with exponential backoff
- Query timeout: Return timeout error with suggestions
- Permission errors: Log and show user-friendly message
- Network issues: Circuit breaker after 5 consecutive failures

---

#### **Integration 2: SSO Provider (SAML/OAuth2)**

**Supported Providers**:
- Azure Active Directory (SAML 2.0)
- Okta (SAML 2.0 / OAuth 2.0)
- Google Workspace (OAuth 2.0)
- Generic SAML 2.0

**Authentication Flow**:
```
User → Streamlit App → SSO Login Page → Authentication → Callback → App Session
   1. User accesses app
   2. App redirects to SSO login
   3. User enters credentials + MFA
   4. SSO returns SAML assertion / OAuth token
   5. App validates assertion
   6. App creates session with user_id, roles
   7. User accesses application
```

**Configuration**:
```yaml
# config/security.yaml
sso:
  enabled: true
  provider: azure_ad
  saml:
    entity_id: "https://app.example.com"
    acs_url: "https://app.example.com/saml/acs"
    sso_url: "https://login.microsoftonline.com/.../saml2"
    x509_cert: "${SAML_CERT}"
  role_mapping:
    "App Admin": admin
    "Data Analyst": analyst
    "Report Viewer": viewer
```

**Implementation**:
```python
# src/ui/auth.py

from onelogin.saml2.auth import OneLogin_Saml2_Auth

class SSOAuthenticator:
    def __init__(self, config: SSOConfig):
        self.config = config
    
    def initiate_login(self):
        auth = OneLogin_Saml2_Auth(request, self.config)
        return auth.login(return_to=self.config.callback_url)
    
    def process_callback(self, request):
        auth = OneLogin_Saml2_Auth(request, self.config)
        auth.process_response()
        
        if auth.is_authenticated():
            user_info = auth.get_attributes()
            return UserSession(
                user_id=user_info['user_id'],
                username=user_info['username'],
                email=user_info['email'],
                roles=self._map_roles(user_info['roles'])
            )
        else:
            raise AuthenticationError(auth.get_errors())
```

---

#### **Integration 3: SIEM / Log Aggregation**

**Supported Systems**:
- Splunk
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Azure Monitor / Log Analytics
- File-based (fallback)

**Log Format**: Structured JSON

```json
{
  "timestamp": "2025-10-29T08:15:23.123Z",
  "level": "INFO",
  "logger": "query_processor",
  "event": "query_executed",
  "user_id": "sarah.jones",
  "session_id": "sess_abc123",
  "query_id": "q_xyz789",
  "query_text": "How many patients admitted yesterday?",
  "sql_text": "SELECT COUNT(*) FROM encounters...",
  "execution_time_ms": 823,
  "row_count": 1,
  "success": true,
  "tables_accessed": ["encounters"],
  "ip_address": "10.0.1.42"
}
```

**Shipping Method**:
```python
# src/utils/logger.py

import structlog
import logging
from pythonjsonlogger import jsonlogger

def setup_logging():
    # JSON formatter
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    log_handler.setFormatter(formatter)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
```

**Splunk Forwarder** (if applicable):
```
# /opt/splunkforwarder/etc/system/local/inputs.conf
[monitor:///var/log/sql-rag-ollama/*.log]
disabled = false
sourcetype = json
index = application_logs
```

---

#### **Integration 4: Monitoring (Prometheus + Grafana)**

**Metrics Exposed**:

```python
# src/utils/metrics.py

from prometheus_client import Counter, Histogram, Gauge

# Query metrics
query_total = Counter('queries_total', 'Total queries processed', ['status', 'intent'])
query_duration = Histogram('query_duration_seconds', 'Query processing time', ['stage'])
active_users = Gauge('active_users', 'Current active users')

# LLM metrics
llm_requests = Counter('llm_requests_total', 'Total LLM requests', ['model'])
llm_duration = Histogram('llm_inference_seconds', 'LLM inference time')
llm_tokens = Histogram('llm_tokens_generated', 'Tokens generated per request')

# Database metrics
db_queries = Counter('db_queries_total', 'Database queries executed', ['status'])
db_duration = Histogram('db_query_seconds', 'Database query execution time')
db_connections = Gauge('db_connection_pool_active', 'Active database connections')

# Cache metrics
cache_hits = Counter('cache_hits_total', 'Cache hits')
cache_misses = Counter('cache_misses_total', 'Cache misses')

# Usage in code
@query_duration.labels(stage='sql_generation').time()
async def generate_sql(...):
    ...
    query_total.labels(status='success', intent='count').inc()
```

**Prometheus Scrape Config**:
```yaml
# monitoring/prometheus.yml
scrape_configs:
  - job_name: 'sql-rag-ollama'
    static_configs:
      - targets: ['localhost:8000']  # Metrics endpoint
    scrape_interval: 15s
```

**Grafana Dashboard**:
- Query latency (p50, p95, p99)
- Query success rate
- Active users over time
- LLM inference time
- Database query distribution
- Cache hit rate
- Error rate by type

---

### **8.2 Internal Module Integration**

**Module Dependency Graph**:

```
┌─────────────────────────────────────────────────────┐
│                      UI Module                      │
│              (Streamlit Interface)                  │
└───────────────────────┬─────────────────────────────┘
                        │ depends on
                        ▼
┌─────────────────────────────────────────────────────┐
│                   Core Module                       │
│            (QueryProcessor - Orchestrator)          │
└───┬───────────┬───────────┬───────────┬─────────────┘
    │           │           │           │
    │depends on │           │           │depends on
    ▼           ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
│  RAG   │ │  LLM   │ │Database│ │Validation│
│ Module │ │ Module │ │ Module │ │  Module  │
└────────┘ └────────┘ └────────┘ └──────────┘
    │           │           │
    │depends on │           │depends on
    ▼           ▼           ▼
┌───────────────────────────────────────────┐
│         Infrastructure Module             │
│  (Logging, Config, Metrics, Cache)        │
└───────────────────────────────────────────┘
```

**Dependency Injection**:

```python
# src/main.py - Application Bootstrap

from src.core.query_processor import QueryProcessor
from src.rag.rag_engine import RAGEngine
from src.llm.llm_engine import LLMEngine
from src.database.database_engine import DatabaseEngine
from src.validation.query_validator import QueryValidator
from src.core.conversation_manager import ConversationManager

def build_application():
    """
    Dependency Injection: Construct application with all dependencies.
    This enables testing (mock dependencies) and modularity.
    """
    # Load configuration
    config = load_config()
    
    # Infrastructure layer
    logger = setup_logging(config.logging)
    metrics = MetricsCollector()
    cache = CacheService(config.cache)
    
    # Database layer
    db_engine = DatabaseEngine(
        config=config.database,
        logger=logger,
        metrics=metrics
    )
    
    # RAG layer
    vector_store = VectorStore(config.rag.vector_store_path)
    embedding_generator = EmbeddingGenerator(config.rag.embedding_model)
    rag_engine = RAGEngine(
        vector_store=vector_store,
        embedding_generator=embedding_generator,
        config=config.rag
    )
    
    # LLM layer
    ollama_client = OllamaClient(config.ollama.base_url)
    prompt_builder = PromptBuilder()
    llm_engine = LLMEngine(
        ollama_client=ollama_client,
        prompt_builder=prompt_builder,
        config=config.ollama
    )
    
    # Validation layer
    schema_provider = SchemaProvider(db_engine)
    validator = QueryValidator(
        schema_provider=schema_provider,
        config=config.validation
    )
    
    # Core layer
    conversation_manager = ConversationManager()
    query_processor = QueryProcessor(
        rag_engine=rag_engine,
        llm_engine=llm_engine,
        validator=validator,
        db_engine=db_engine,
        conversation_manager=conversation_manager
    )
    
    # Wrap with caching
    cached_processor = CachedQueryProcessor(
        processor=query_processor,
        cache=cache
    )
    
    return Application(
        query_processor=cached_processor,
        db_engine=db_engine,
        config=config
    )
```

---

## **9. Deployment Architecture**

### **9.1 Single-Server Deployment (MVP)**

```
┌─────────────────────────────────────────────────────────────┐
│               Physical Server / VM                          │
│  OS: Ubuntu 22.04 LTS                                       │
│  Resources: 16GB RAM, 8-core CPU, 100GB SSD                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Docker Container: sql-rag-ollama-app               │    │
│  │ Port: 8501 (Streamlit)                             │    │
│  │ Volumes: ./data, ./config, ./logs                  │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Docker Container: ollama                           │    │
│  │ Port: 11434 (Ollama API)                           │    │
│  │ Volume: ./models                                   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Systemd Service: prometheus                        │    │
│  │ Port: 9090 (Metrics)                               │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  Data Directories (Host):                                  │
│  • /opt/sql-rag-ollama/data/vector_db/                     │
│  • /opt/sql-rag-ollama/data/logs/                          │
│  • /opt/sql-rag-ollama/data/schemas/                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
            │
            │ Network
            ▼
┌─────────────────────────────────────┐
│  SQL Server (Separate Server)      │
│  Port: 1433                         │
│  User: readonly_user                │
└─────────────────────────────────────┘
```

**Docker Compose**:
```yaml
# deployment/docker/docker-compose.yml

version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ./models:/root/.ollama
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  app:
    build:
      context: ../..
      dockerfile: deployment/docker/Dockerfile
    container_name: sql-rag-ollama-app
    ports:
      - "8501:8501"
      - "8000:8000"  # Metrics endpoint
    volumes:
      - ../../data:/app/data
      - ../../config:/app/config
      - ../../logs:/app/logs
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - DB_HOST=${DB_HOST}
      - DB_PORT=${DB_PORT}
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
    depends_on:
      - ollama
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ../../monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

volumes:
  prometheus_data:
```

---

### **9.2 Production Deployment with High Availability**

```
┌───────────────────────────────────────────────────────────┐
│                     Load Balancer                         │
│                    (HAProxy / Nginx)                      │
│                    health checks enabled                  │
└────────────────┬────────────────┬─────────────────────────┘
                 │                │
                 ▼                ▼
         ┌─────────────┐  ┌─────────────┐
         │   Server 1  │  │   Server 2  │
         │   (Active)  │  │  (Active)   │
         │             │  │             │
         │ • App       │  │ • App       │
         │ • Ollama    │  │ • Ollama    │
         └─────────────┘  └─────────────┘
         │      │                │
         │      └────────┬───────┘
         │               │
         │               ▼
         │   ┌────────────────────────┐
         │   │    Redis Cluster       │
         │   │  • Session storage     │
         │   │  • Query cache         │
         │   │  • Rate limiting       │
         │   └────────────────────────┘
         │               │
         └───────────────┼────────────────┐
                         │                │
                         ▼                ▼
                ┌──────────────┐  ┌──────────────┐
                │  ChromaDB    │  │ PostgreSQL   │
                │  (Vector DB) │  │ (App State)  │
                └──────────────┘  └──────────────┘
                        │
                        ▼
                ┌──────────────────┐
                │   SQL Server     │
                │ Read Replica Pool│
                │ (Load Balanced)  │
                └──────────────────┘
```

**High Availability Features**:
- **Load Balancer**: Health checks, automatic failover
- **Stateless App Servers**: Session in Redis, not memory
- **Database Replication**: Read replicas for query load
- **Shared Storage**: NFS or S3 for vector store
- **Auto-Recovery**: Kubernetes or Docker Swarm orchestration

---

### **9.3 Kubernetes Deployment (Enterprise Scale)**

```yaml
# deployment/kubernetes/deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: sql-rag-ollama-app
  namespace: analytics
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sql-rag-ollama
  template:
    metadata:
      labels:
        app: sql-rag-ollama
    spec:
      containers:
      - name: app
        image: sql-rag-ollama:1.0.0
        ports:
        - containerPort: 8501
          name: http
        - containerPort: 8000
          name: metrics
        env:
        - name: OLLAMA_HOST
          value: "http://ollama-service:11434"
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: password
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 15
          periodSeconds: 5
        volumeMounts:
        - name: data
          mountPath: /app/data
        - name: config
          mountPath: /app/config
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: sql-rag-data-pvc
      - name: config
        configMap:
          name: sql-rag-config

---
apiVersion: v1
kind: Service
metadata:
  name: sql-rag-service
  namespace: analytics
spec:
  selector:
    app: sql-rag-ollama
  ports:
  - name: http
    port: 80
    targetPort: 8501
  - name: metrics
    port: 8000
    targetPort: 8000
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sql-rag-hpa
  namespace: analytics
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sql-rag-ollama-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

### **9.4 Deployment Pipeline (CI/CD)**

```yaml
# .github/workflows/deploy.yml

name: Build and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      
      - name: Run linters
        run: |
          ruff check src/
          mypy src/
      
      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: |
          docker build -t sql-rag-ollama:${{ github.sha }} .
          docker tag sql-rag-ollama:${{ github.sha }} sql-rag-ollama:latest
      
      - name: Push to registry
        run: |
          echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USERNAME }} --password-stdin
          docker push sql-rag-ollama:${{ github.sha }}
          docker push sql-rag-ollama:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/sql-rag-ollama-app \
            app=sql-rag-ollama:${{ github.sha }} \
            --namespace=staging
          kubectl rollout status deployment/sql-rag-ollama-app --namespace=staging
      
      - name: Run smoke tests
        run: |
          python scripts/deployment/smoke_test.py --env staging
      
      - name: Deploy to production
        if: success()
        run: |
          kubectl set image deployment/sql-rag-ollama-app \
            app=sql-rag-ollama:${{ github.sha }} \
            --namespace=production
          kubectl rollout status deployment/sql-rag-ollama-app --namespace=production
```

---

## **10. Reflection and Architectural Decisions**

### **10.1 Architectural Decisions Justification**

#### **Decision 1: Modular Monolith over Microservices**

**Justification**:
- **Scale Match**: 10-20 concurrent users don't justify microservices complexity
- **Operational Simplicity**: Healthcare IT teams prefer simpler deployments
- **Development Velocity**: Single codebase accelerates feature development
- **HIPAA Compliance**: Fewer components = simpler security audit
- **Cost Efficiency**: Single server deployment vs complex orchestration

**Alternative Considered**: Microservices architecture
- **Pros**: Better scalability, technology flexibility
- **Cons**: Operational overhead, network latency, complexity overkill
- **Why Rejected**: Scale doesn't warrant complexity; can extract services later if needed

**Evolution Path**: Modular boundaries enable future service extraction
```python
# Current: In-process module call
result = await rag_engine.retrieve_context(query)

# Future: REST API call (if needed)
result = await rag_service_client.get("/context", params={"query": query})
```

---

#### **Decision 2: Ollama over Cloud LLM APIs**

**Justification**:
- **Privacy Requirement**: HIPAA mandates local processing; cloud APIs violate this
- **Cost Predictability**: No per-query charges; one-time hardware cost
- **Network Independence**: Works in air-gapped environments
- **Data Sovereignty**: Patient data never leaves organization
- **Control**: Own the model, update schedule, deployment

**Alternative Considered**: Azure OpenAI, AWS Bedrock, Google Vertex AI
- **Pros**: Better models (GPT-4), no infrastructure management
- **Cons**: Data privacy violations, ongoing costs, internet dependency
- **Why Rejected**: Non-negotiable privacy requirement

**Trade-offs Accepted**:
- ⚠️ Lower accuracy (85% vs 90% with GPT-4)
- ⚠️ Slower inference (2-3s vs 1-2s with cloud)
- ⚠️ Hardware requirements (16GB RAM minimum)

**Mitigation**:
- Use best local model (SQLCoder-7B specialized for SQL)
- RAG compensates for lower model capability
- Quantization (Q4) balances speed and accuracy

---

#### **Decision 3: ChromaDB over Weaviate/Pinecone**

**Justification**:
- **Embedded Deployment**: Runs in-process, no separate server
- **Simplicity**: Zero-configuration for MVP
- **Python-Native**: Clean Python API, no gRPC/REST overhead
- **Sufficient Scale**: Handles 10K+ schema elements easily
- **Local-Only**: Aligns with privacy requirements

**Alternative Considered**: Weaviate (production-grade vector DB)
- **Pros**: Better performance, built for scale, advanced features
- **Cons**: Separate server, operational complexity, overkill for MVP
- **Why Rejected**: Complexity outweighs benefits at this scale

**Evolution Path**:
```python
# Abstraction enables future swap
class VectorStore(ABC):
    @abstractmethod
    async def search(self, embedding, top_k): ...

class ChromaDBStore(VectorStore): ...
class WeaviateStore(VectorStore): ...  # Future
```

---

#### **Decision 4: Streamlit over FastAPI + React**

**Justification**:
- **Development Speed**: UI in hours vs weeks
- **Python-Only**: No context switching to JavaScript
- **Built-in Features**: Session management, caching, components
- **Rapid Iteration**: Live reload, quick prototyping
- **Team Skillset**: Python developers, not frontend specialists

**Alternative Considered**: FastAPI backend + React frontend
- **Pros**: Better performance, more control, scalable to 1000+ users
- **Cons**: 10x development time, requires frontend expertise, overkill for MVP
- **Why Rejected**: Speed-to-market priority; can migrate later

**Migration Strategy** (if needed):
1. Business logic already separate from UI
2. Create FastAPI endpoints exposing `QueryProcessor`
3. Build React frontend consuming API
4. Gradual migration (Streamlit → FastAPI incrementally)

**Trade-offs Accepted**:
- ⚠️ Limited to ~100 concurrent users
- ⚠️ Less control over UI behavior
- ⚠️ Streamlit-specific quirks

---

#### **Decision 5: SQLAlchemy for Schema Introspection Only**

**Justification**:
- **Schema Inspection**: Excellent for extracting metadata
- **Connection Pooling**: Battle-tested pool implementation
- **Database Agnostic**: Easy to support PostgreSQL/MySQL later
- **No ORM Overhead**: Use raw SQL for queries (not ORM)

**Alternative Considered**: Pure pyodbc without SQLAlchemy
- **Pros**: Simpler, fewer dependencies
- **Cons**: Manual connection pooling, database-specific schema queries
- **Why Rejected**: SQLAlchemy provides value without ORM baggage

**Usage Pattern**:
```python
# Use SQLAlchemy for schema introspection
from sqlalchemy import inspect, create_engine

engine = create_engine(connection_string)
inspector = inspect(engine)
tables = inspector.get_table_names()

# Use raw SQL for actual queries (bypass ORM)
with engine.connect() as conn:
    result = conn.execute(text(generated_sql))
```

---

### **10.2 Risk Assessment and Mitigation**

#### **Risk 1: LLM Hallucination Produces Incorrect SQL**

**Likelihood**: High (20-30% of queries without mitigation)  
**Impact**: Critical (wrong answers destroy user trust)  
**Risk Score**: **CRITICAL**

**Mitigation Layers**:
1. **RAG Context**: Ground generation in actual schema (reduces hallucination 50%)
2. **Schema Validation**: Catch non-existent tables/columns before execution
3. **SQL Linting**: Parse and validate SQL syntax
4. **User Review**: Display SQL for verification
5. **Confidence Scoring**: Warn on low-confidence generations
6. **Example Learning**: Store successful queries as examples

**Residual Risk**: 5-10% incorrect queries reach execution
**Acceptance**: Show SQL to users; they can spot obvious errors

---

#### **Risk 2: Performance Degradation Under Load**

**Likelihood**: Medium (as usage grows)  
**Impact**: High (slow = abandoned)  
**Risk Score**: **HIGH**

**Mitigation**:
1. **Caching**: 5-minute TTL for repeated queries (50% hit rate expected)
2. **Connection Pooling**: Prevent database connection overhead
3. **Query Optimization**: Add MAXDOP hints, TOP clauses
4. **Request Queuing**: Graceful degradation vs crashes
5. **Horizontal Scaling**: Architecture supports adding servers

**Monitoring**:
- P95 latency alerts (threshold: 7 seconds)
- Queue depth alerts (threshold: 10 waiting)
- Automatic scaling in Kubernetes

**Residual Risk**: Complex queries may still be slow (10-15s)
**Acceptance**: Warn users before executing complex queries

---

#### **Risk 3: Schema Changes Break Queries**

**Likelihood**: Medium (schema changes monthly)  
**Impact**: Medium (frustrating but recoverable)  
**Risk Score**: **MEDIUM**

**Mitigation**:
1. **Daily Schema Refresh**: Detect changes within 24 hours
2. **Change Notifications**: Alert admins on schema changes
3. **Version Control**: Snapshot schemas for rollback
4. **Graceful Degradation**: Suggest alternatives for missing tables
5. **Schema Aliases**: Map old names to new names

**Example**:
```python
# Schema change detected
if table_not_found('encounters'):
    # Check aliases
    new_name = schema_alias_map.get('encounters')
    if new_name:
        return f"Table 'encounters' renamed to '{new_name}'. Query updated."
```

**Residual Risk**: Breaking changes (dropped columns) can't be auto-fixed
**Acceptance**: Manual query updates required for major schema changes

---

#### **Risk 4: Security Vulnerability Exploitation**

**Likelihood**: Low (with proper controls)  
**Impact**: Critical (HIPAA violation, data breach)  
**Risk Score**: **HIGH**

**Mitigation**:
1. **Multi-Layer Validation**: 5 validation gates before execution
2. **Read-Only User**: Database account cannot modify data
3. **Input Sanitization**: Block injection patterns
4. **Audit Logging**: Complete trail for forensics
5. **Regular Security Audits**: Quarterly penetration testing
6. **Dependency Scanning**: Weekly CVE checks

**Attack Scenarios**:
- **SQL Injection**: Blocked by validation layer 1
- **Prompt Injection**: LLM generates harmful SQL → Blocked by layer 2
- **Privilege Escalation**: Read-only user prevents modification
- **Data Exfiltration**: Audit logs detect unusual access patterns

**Residual Risk**: Zero-day vulnerabilities in dependencies
**Acceptance**: Rapid patching process; security mailing list monitoring

---

#### **Risk 5: Dependency on Ollama Project**

**Likelihood**: Low (active project)  
**Impact**: High (core technology)  
**Risk Score**: **MEDIUM**

**Mitigation**:
1. **Abstraction Layer**: LLM interface enables runtime swapping
2. **Fallback Options**: llama.cpp, vLLM documented as alternatives
3. **Model Portability**: GGUF format works across runtimes
4. **Community**: Large community reduces abandonment risk
5. **Fork Option**: Open source; can fork if needed

**Backup Plan**:
```python
# LLM abstraction enables swap
class OllamaLLMProvider(LLMProvider):
    def generate(self, prompt): ...

class LlamaCppProvider(LLMProvider):  # Fallback
    def generate(self, prompt): ...

# Configuration switch
llm_provider = (OllamaLLMProvider() 
                if config.llm.provider == 'ollama' 
                else LlamaCppProvider())
```

---

### **10.3 Future-Proofing and Extensibility**

#### **Extensibility Point 1: Multi-Database Support**

**Current State**: Single SQL Server database  
**Future Need**: PostgreSQL, MySQL, Oracle support

**Architecture Preparation**:
```python
# Database adapter pattern (already implemented)

class DatabaseAdapter(ABC):
    @abstractmethod
    async def get_schema(self): ...
    
    @abstractmethod
    async def execute_query(self, sql): ...
    
    @abstractmethod
    def generate_sql_dialect(self) -> str: ...

class SQLServerAdapter(DatabaseAdapter): ...
class PostgreSQLAdapter(DatabaseAdapter): ...  # Future
class MySQLAdapter(DatabaseAdapter): ...        # Future

# Factory pattern for creation
def create_adapter(config: DatabaseConfig) -> DatabaseAdapter:
    if config.type == 'sqlserver':
        return SQLServerAdapter(config)
    elif config.type == 'postgresql':
        return PostgreSQLAdapter(config)
    # etc.
```

**Migration Path**:
1. Implement adapter for new database
2. Update prompt templates with dialect-specific SQL
3. Test with sample database
4. Deploy as optional configuration

---

#### **Extensibility Point 2: Alternative LLM Models**

**Current State**: Ollama with SQLCoder-7B  
**Future Need**: GPT-4, Claude, custom fine-tuned models

**Architecture Preparation**:
```python
# LLM provider abstraction

class LLMProvider(ABC):
    @abstractmethod
    async def generate_sql(self, prompt: str) -> str: ...

class OllamaProvider(LLMProvider):
    def __init__(self, model: str):
        self.model = model  # 'sqlcoder:7b', 'codellama:13b', etc.

class OpenAIProvider(LLMProvider):  # Future
    def __init__(self, api_key: str, model: str):
        self.client = openai.Client(api_key)
        self.model = model

class AnthropicProvider(LLMProvider):  # Future
    ...

# Configuration-driven selection
llm_config = {
    'provider': 'ollama',  # or 'openai', 'anthropic'
    'model': 'sqlcoder:7b',
    'temperature': 0.1
}
```

**Benefit**: Easy experimentation with different models

---

#### **Extensibility Point 3: Custom Validation Rules**

**Current State**: Hardcoded validation rules  
**Future Need**: Organization-specific rules

**Architecture Preparation**:
```python
# Plugin architecture for validators

class ValidationRule(ABC):
    @abstractmethod
    def validate(self, sql: str) -> List[ValidationIssue]: ...

class SQLInjectionRule(ValidationRule): ...
class ProhibitedOperationRule(ValidationRule): ...

# Custom organization rules
class CustomBusinessHoursRule(ValidationRule):
    """Only allow queries during business hours"""
    def validate(self, sql: str):
        if not is_business_hours():
            return [ValidationIssue(
                level=ValidationLevel.ERROR,
                message="Queries only allowed during business hours"
            )]
        return []

# Load rules from config
rules = [
    SQLInjectionRule(),
    ProhibitedOperationRule(),
    # Load custom rules from plugins/
]
```

---

#### **Extensibility Point 4: UI Framework Migration**

**Current State**: Streamlit  
**Future Need**: FastAPI + React for scale

**Architecture Preparation**:
- Business logic completely separate from UI
- `QueryProcessor` has clean interface (no Streamlit dependencies)
- API-ready: Can expose as REST endpoints

**Migration Path**:
```python
# Step 1: Add FastAPI alongside Streamlit

from fastapi import FastAPI

app = FastAPI()
query_processor = build_query_processor()  # Shared instance

@app.post("/api/query")
async def api_query(request: QueryRequest):
    result = await query_processor.process_query(
        user_query=request.to_user_query(),
        session=await get_session(request.user_id)
    )
    return result.to_dict()

# Step 2: Build React frontend consuming API

# Step 3: Sunset Streamlit gradually
```

---

### **10.4 Impact of AI Utilization**

#### **How AI Influenced Architecture**

**AI Model Consultation Examples**:

**1. Prompt Engineering Strategy**:
```
Query to Claude: "Design prompt structure for text-to-SQL with RAG. 
Consider: schema context, few-shot examples, conversation history, 
token budget constraints."

AI Recommendation: Structured prompt with clear sections
├─ System instruction (role definition)
├─ Schema context (relevant tables/columns)
├─ Few-shot examples (2-3 similar queries)
├─ Conversation context (last 3 turns)
└─ User query

Adopted: Modified to fit 2000 token budget
```

**2. Caching Strategy**:
```
Query to GPT-4: "Multi-tier caching strategy for LLM application.
Components: query results, schema metadata, embeddings.
Requirements: balance freshness vs performance."

AI Recommendation: 3-tier cache (memory → Redis → source)
with appropriate TTLs per data type.

Adopted: Simplified to 2-tier (memory → source) for MVP
Reason: Redis adds complexity; memory sufficient for scale
```

**3. Error Recovery Patterns**:
```
Query to Claude: "SQL generation error recovery strategies.
Errors: table not found, syntax error, timeout.
Goal: automatic retry with improved prompt."

AI Recommendation: Iterative refinement pattern
1. Attempt generation
2. If error, add error message to context
3. Retry with corrected prompt (max 2 retries)
4. If still fails, present error to user with suggestions

Adopted: Full pattern implemented in LLMEngine
```

---

#### **AI Code Generation Benefits**

**Boilerplate Reduction**:
- AI generated 60% of dataclass definitions
- Validation logic patterns AI-suggested
- Test fixtures created by AI (80% accuracy, required cleanup)

**Example**:
```python
# Human prompt: "Create dataclass for query result with validation"

# AI generated (with minor edits):
@dataclass
class QueryResult:
    query_id: str
    success: bool
    rows: List[Dict[str, Any]]
    row_count: int
    execution_time_ms: float
    error_message: Optional[str] = None
    
    def __post_init__(self):
        if self.success and not self.rows:
            raise ValueError("Successful query must have rows")
        if not self.success and not self.error_message:
            raise ValueError("Failed query must have error message")
```

---

#### **AI Limitations Encountered**

**1. Context Window Limits**:
- AI couldn't process entire codebase at once
- Solution: Break into modules, provide summaries

**2. Domain Knowledge Gaps**:
- AI less helpful with healthcare-specific logic
- AI suggestions for HIPAA compliance too generic
- Solution: Human expertise for domain-specific decisions

**3. Code Quality Variance**:
- AI-generated code needed refactoring ~40% of time
- Inconsistent naming conventions
- Solution: Human review and standardization pass

**4. Architectural Creativity**:
- AI good at known patterns, less innovative
- Novel architecture decisions still human-driven
- Solution: Use AI for validation, not primary design

---

### **10.5 Development and Maintenance Considerations**

#### **Developer Onboarding**

**Onboarding Timeline**: 3-5 days for productive contribution

**Day 1: Environment Setup**
```bash
# Automated setup script
./scripts/setup/install_dependencies.sh --dev
./scripts/setup/setup_database.py --mock  # Use mock DB for dev
./scripts/setup/init_vector_store.py --sample-data

# Verify setup
make test-unit
```

**Day 2-3: Architecture Walkthrough**
- Review architecture diagrams
- Read key module READMEs
- Pair program on bug fix (learn codebase)
- Run application locally

**Day 4-5: First Contribution**
- Implement small feature (e.g., new validation rule)
- Write tests
- Submit PR with code review

**Training Materials**:
- Video walkthrough (30 minutes): Architecture overview
- Interactive tutorial: Make your first query
- Documentation: `docs/guides/developer/`

---

#### **Maintenance Effort Estimation**

**Weekly Maintenance** (2-4 hours):
- Dependency updates (automated PR review)
- Security scan review
- Log monitoring for errors
- Performance metric review

**Monthly Maintenance** (1 day):
- Schema refresh review
- Vector store reindexing (if needed)
- Query accuracy analysis
- User feedback review

**Quarterly Maintenance** (1 week):
- Major dependency upgrades
- Security audit
- Performance optimization
- Technical debt reduction sprint

---

#### **Monitoring and Alerting**

**Critical Alerts** (immediate response):
- Application down (health check fails)
- Error rate >5%
- P95 latency >10 seconds
- Database connection failures

**Warning Alerts** (review within 24h):
- Error rate 2-5%
- P95 latency 7-10 seconds
- Disk usage >80%
- Query accuracy <80%

**Info Alerts** (weekly review):
- Schema changes detected
- New user signups
- Usage pattern changes
- Performance trends

**Alert Configuration**:
```yaml
# monitoring/alerts.yml

alerts:
  - name: HighErrorRate
    condition: error_rate > 0.05
    severity: critical
    notification: pagerduty
    
  - name: SlowQueries
    condition: p95_latency > 10
    severity: warning
    notification: slack
    
  - name: DiskSpaceWarning
    condition: disk_usage > 0.80
    severity: warning
    notification: email
```

---

#### **Technical Debt Management**

**Prevention**:
- Code review mandatory (no direct commits to main)
- Test coverage enforcement (80% minimum)
- Automated linting (ruff, mypy, pylint)
- "Definition of Done" includes refactoring

**Tracking**:
```python
# Technical Debt Register (docs/technical-debt.md)

## TD-001: Conversation context storage
- Issue: Currently in-memory, lost on restart
- Impact: Medium (user experience)
- Effort: 2 days (implement Redis storage)
- Priority: P2 (next quarter)

## TD-002: SQL parser for accurate table extraction
- Issue: Regex-based, misses complex queries
- Impact: Low (rare edge cases)
- Effort: 5 days (integrate SQL parser library)
- Priority: P3 (backlog)
```

**Allocation**: 20% of sprint capacity to debt reduction

---

#### **Disaster Recovery**

**Backup Strategy**:
```bash
# Daily automated backup
0 1 * * * /opt/sql-rag-ollama/scripts/maintenance/backup_data.sh

# Backup contents:
- Vector store (ChromaDB data)
- Query history database
- Configuration files
- Schema snapshots (last 30 days)

# Backup location:
- Primary: /backups/sql-rag-ollama/
- Secondary: S3/Azure Blob (encrypted)
- Retention: 30 days daily, 12 months weekly
```

**Recovery Time Objective (RTO)**: 4 hours  
**Recovery Point Objective (RPO)**: 24 hours (daily backups)

**Recovery Procedure**:
```bash
# 1. Restore from backup
./scripts/maintenance/restore_data.sh /backups/sql-rag-ollama/2025-10-29.tar.gz

# 2. Verify data integrity
./scripts/maintenance/verify_restore.py

# 3. Restart services
docker-compose restart

# 4. Run health checks
./scripts/deployment/health_check.py

# 5. Notify users of restoration
```

---

## **11. Architecture Summary and Conclusion**

### **11.1 Architecture Highlights**

**Core Architectural Strengths**:

1. **Modular Monolith Design**: Simplicity of monolith with flexibility of modules
2. **Privacy-First**: Local processing satisfies HIPAA without compromise
3. **Defense-in-Depth Security**: 6 security layers from network to audit
4. **Scalability Path**: Start simple, scale when needed (vertical → horizontal)
5. **Technology Maturity**: Battle-tested stack (Python, PostgreSQL, Ollama)
6. **Extensibility Points**: Plugin architecture for validators, adapters, providers
7. **Observable**: Comprehensive logging, metrics, health checks
8. **Developer-Friendly**: Clear structure, good documentation, fast onboarding

---

### **11.2 Key Metrics and Targets**

**Performance Targets**:
- Query response: <5 seconds (P95)
- LLM inference: <3 seconds
- Database query: <2 seconds
- Vector retrieval: <500ms

**Quality Targets**:
- SQL accuracy: >85%
- Test coverage: >80%
- Query success rate: >90%
- Uptime: 99.5% (business hours)

**Scale Targets**:
- Concurrent users: 10-20 (Phase 1), 50+ (Phase 2)
- Database tables: <1000
- Queries per day: 500-1000
- Schema refresh: Daily

---

### **11.3 From Architecture to Implementation**

**Readiness Assessment**:

✅ **Ready for Implementation**:
- Technology stack decided and justified
- Component interfaces defined
- Data models specified
- Security architecture complete
- Deployment strategy defined

⚠️ **Needs Refinement**:
- Prompt engineering templates (iterative improvement)
- Performance optimization specifics (measure first)
- Error recovery edge cases (discover in testing)

**Next Steps**:

**Phase 1: Foundation (Weeks 1-2)**
```
Week 1: Infrastructure Setup
├─ Set up development environment
├─ Install Ollama, pull models
├─ Configure database connection
└─ Initialize vector store

Week 2: Core Pipeline
├─ Implement QueryProcessor skeleton
├─ Basic LLM integration (simple prompts)
├─ Database query execution
└─ End-to-end smoke test
```

**Phase 2: RAG Integration (Weeks 3-4)**
```
Week 3: Schema Ingestion
├─ Schema extraction from database
├─ Embedding generation
├─ Vector store indexing
└─ Retrieval testing

Week 4: RAG-Enhanced Generation
├─ Context retrieval in pipeline
├─ Prompt building with context
├─ Accuracy testing and iteration
└─ Example query library
```

**Phase 3: Validation & UI (Weeks 5-6)**
```
Week 5: Security Validation
├─ Multi-layer validation implementation
├─ SQL injection testing
├─ Schema validation
└─ Security audit

Week 6: User Interface
├─ Streamlit UI implementation
├─ Result display components
├─ History management
└─ User testing
```

**Phase 4: Refinement & Deploy (Weeks 7-8)**
```
Week 7: Testing & Optimization
├─ Integration testing
├─ Performance optimization
├─ Load testing
└─ Bug fixes

Week 8: Deployment
├─ Production setup
├─ Data migration
├─ User training
└─ Go-live
```

---

### **11.4 Success Criteria**

**Technical Success**:
- [x] Architecture document complete and reviewed
- [ ] All components implemented and tested
- [ ] Performance targets met (P95 <5s)
- [ ] Security audit passed
- [ ] 80%+ test coverage achieved

**User Success**:
- [ ] 80%+ of queries answered correctly
- [ ] User satisfaction >4.0/5.0
- [ ] 75%+ weekly active user rate
- [ ] <10% support ticket rate

**Business Success**:
- [ ] 50% reduction in IT report request time
- [ ] 30+ active users within 3 months
- [ ] ROI positive within 6 months
- [ ] Zero HIPAA compliance violations

---

### **11.5 Final Reflection**

This architecture represents a **pragmatic balance** between:
- **Simplicity** (modular monolith) and **scalability** (clear evolution path)
- **Security** (defense-in-depth) and **usability** (fast queries)
- **Innovation** (LLM-powered) and **reliability** (proven technologies)
- **Speed** (MVP in 8 weeks) and **quality** (comprehensive testing)

The architecture acknowledges **what we know**:
- Healthcare requires HIPAA compliance
- Local processing is non-negotiable
- Team has Python expertise
- Users need simple interface

And **what we don't know**:
- Actual query patterns (will learn in production)
- Performance at scale (can optimize later)
- User preferences (will iterate based on feedback)

**The design enables learning**: Modular structure allows easy changes based on real-world usage. This is not a rigid blueprint but a **living architecture** that evolves with the product.

**Most importantly**: The architecture directly serves the mission of **democratizing data access in healthcare**. Every decision—from local LLM deployment to conversational UI to comprehensive validation—traces back to making data accessible to non-technical healthcare workers while maintaining the trust and security their work demands.

---

**Architecture Status**: ✅ **COMPLETE - READY FOR PSEUDOCODE PHASE**

**Next Phase**: SPARC Phase 4 - Pseudocode (Algorithm Design)

**Approval Required From**:
- [ ] Technical Lead (architecture review)
- [ ] Security Team (security architecture approval)
- [ ] IT Operations (deployment feasibility)
- [ ] Product Owner (alignment with requirements)

---

**Document Version**: 1.0  
**Last Updated**: October 29, 2025  
**Authors**: Development Team + AI-Assisted Design  
**Status**: Final - Awaiting Stakeholder Approval