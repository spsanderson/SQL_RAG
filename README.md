# SQL RAG
Using LLMs and RAG against SQL

Summary:

**Documents Analyzed:**

  * **TITLE:** [`SPARC Document`](SPARC_Documents/SQL%20LLM%20RAG%20Project%20SPARC.md)
  * **TITLE:** [`1_Functional Requirements.md`](SPARC_Documents/1_Functional%20Requirements.md)
  * **TITLE:** [`2_NonFunctional_Requirements.md`](SPARC_Documents/2_NonFunctional_Requirements.md)
  * **TITLE:** [`3_User_Scenarios.md`](SPARC_Documents/3_User_Scenarios.md)
  * **TITLE:** [`4_UIUX_Requirements.md`](SPARC_Documents/4_UIUX_Requirements.md)
  * **TITLE:** [`5_File_Structure.md`](SPARC_Documents/5_File_Structure.md)
  * **TITLE:** [`6_Assumptions_Requirements.md`](SPARC_Documents/6_Assumptions_Requirements.md)
  * **TITLE:** [`7_Reflection.md`](SPARC_Documents/7_Reflection.md)
  * **TITLE:** [`Pseudocode Document`](SPARC_Documents/Pseudocode_Requirements.md)
  * **TITLE:** [`Architecture_Requirements.md`](SPARC_Documents/Architecture_Requirements.md)
  * **TITLE:** [`Refinement Document`](SPARC_Documents/Refinement_Document.md)
  * **TITLE:** [`Completion_Document.md`](SPARC_Documents/Completion_Document.md)

**List of Filenames:**

```
[
  "SQL LLM RAG Project SPARC.md",
  "1_Functional Requirements.md",
  "2_NonFunctional_Requirements.md",
  "3_User_Scenarios.md",
  "4_UIUX_Requirements.md",
  "5_File_Structure.md",
  "6_Assumptions_Requirements.md",
  "7_Reflection.md",
  "Pseudocode Requirements.md",
  "Architecture_Requirements.md",
  "Refinement_Document.md",
  "Completion_Document.md"
]
```

-----

## 📄 Document Summaries for README

Here are summaries for each specification document.

### Functional Requirements (`1_Functional Requirements.md`)

This document outlines **what the system must do**. It details the specific functions, features, and capabilities required for the SQL RAG Ollama application. Key areas include:

  * Accepting and processing **natural language queries** (FR-1).
  * Generating accurate **SQL queries** (T-SQL dialect) based on user intent (FR-2).
  * Utilizing **Retrieval-Augmented Generation (RAG)** to fetch relevant database schema context (FR-3).
  * Interacting with the local **Ollama LLM** via structured prompts (FR-4).
  * Implementing strict **query validation and safety checks** (FR-5).
  * Executing SQL queries and handling results (FR-6).
  * Managing database **schema extraction and refresh** (FR-7).
  * Maintaining **conversation context** for follow-up queries (FR-8).
  * Presenting results clearly and enabling **data export** (FR-9).
  * Defining necessary **User Interface components** (FR-10).
  * Providing an **example query library** (FR-11).
  * Ensuring comprehensive **logging and audit trails** (FR-12).
    Requirements are prioritized using the MoSCoW method.

-----

### Non-Functional Requirements (`2_NonFunctional_Requirements.md`)

This document specifies **how the system should perform** its functions, defining quality attributes, constraints, and operational characteristics. It focuses on:

  * **Performance (NFR-1):** Sets targets for query response times (e.g., \< 3s for simple queries), LLM inference speed (≥ 30 tokens/sec), database execution limits (30s timeout), and concurrency (10-20 users).
  * **Security & Privacy (NFR-2):** Mandates **local-only processing** (no external APIs), HIPAA compliance, PHI protection, robust authentication/authorization (SSO, RBAC), SQL injection prevention, and comprehensive audit logging (6+ year retention).
  * **Reliability & Availability (NFR-3):** Defines uptime targets (99.5% business hours), fault tolerance strategies (graceful degradation), data integrity measures, and error recovery mechanisms (automatic retries).
  * **Scalability (NFR-4):** Outlines plans for scaling users (up to 100+), data volume (thousands of tables), and query complexity.
  * **Maintainability (NFR-5):** Specifies code quality standards (80%+ test coverage, linting), documentation requirements, observability needs (structured logging, metrics), and configuration management.
  * **Usability (NFR-6):** Focuses on learnability (\< 5 min to first query), efficiency (keyboard shortcuts), accessibility (WCAG 2.1 AA), and user satisfaction (SUS ≥ 75).
  * **Compatibility (NFR-7):** Defines supported browsers, server OS, and SQL Server versions (2016+).
  * **Portability (NFR-8):** Ensures deployment flexibility (Docker, VM) and data portability (export/import).

-----

### User Scenarios (`3_User_Scenarios.md`)

This document describes **realistic situations** where different users interact with the system to achieve specific goals, illustrating the practical application of the functional requirements. It includes:

  * **Eight detailed scenarios** covering various user personas and tasks:
    1.  **Sarah (Ops Manager):** Simple daily report query with follow-up.
    2.  **Mark (Analyst):** Complex analytical query (readmissions) with template saving.
    3.  **Dr. Johnson (Physician):** Error recovery from incorrect terminology ("HCAHPS").
    4.  **New Hire:** First-time user onboarding and tutorial flow.
    5.  **Sarah (Returning):** Query refinement through conversation context.
    6.  **Mark (Analyst):** Data export and report scheduling.
    7.  **New Analyst:** Schema exploration and discovery.
    8.  **IT Admin:** System configuration and monitoring.
  * **User Flows:** Step-by-step interactions, system responses, decision points, and UI states.
  * **Alternative Flows:** Handling ambiguities, validation failures, and timeouts.
  * **Flow Diagrams:** Visual representations of the user journeys.
  * **Decision Matrix:** Summarizes key system behaviors in different situations.
    These scenarios inform UI/UX design, testing strategies, and feature prioritization.

-----

### UI/UX Requirements (`4_UIUX_Requirements.md`)

This document defines the **design principles, visual language, interaction patterns, and accessibility standards** for the user interface, aiming for clarity, efficiency, and ease of use. Key aspects include:

  * **Core Design Principles:** Clarity over cleverness, progressive disclosure, immediate feedback, error prevention, consistency, and recognition over recall.
  * **Visual Design System:** Defines the color palette (primary blue, semantic colors), typography (system fonts, type scale), spacing (8-point grid), and elevation (shadow system).
  * **Interface Layout:** Wireframes for desktop (sidebar + main content) and mobile (tab bar) layouts.
  * **Component Design:** Detailed specifications for key components like the query input box (with states like autocomplete, loading, error), results display (SQL, natural language answer, data table), sidebar navigation (collapsible), and modal dialogs.
  * **Accessibility Standards:** Commits to **WCAG 2.1 Level AA**, covering perceivable (alt text, semantics), operable (keyboard navigation, focus), understandable (predictability, input assistance), and robust (valid HTML, ARIA) requirements.
  * **Component Patterns:** Defines styles and states for buttons, input fields, toast notifications, and loading indicators.
  * **Implementation Guidelines:** Recommends CSS architecture (BEM, utility classes), responsive design strategy (mobile-first), and animation principles.

-----

### File Structure (`5_File_Structure.md`)

This document proposes a **standardized directory structure** for the project codebase, documentation, configuration, and other assets, promoting modularity and maintainability. It outlines:

  * **Root Directory:** Top-level folders including `.github` (CI/CD), `docs` (documentation), `src` (source code), `tests` (testing), `config` (configuration), `data` (storage, gitignored), `scripts` (automation), `monitoring` (observability), `deployment` (Docker, K8s), `migrations` (database), and standard project files (`README.md`, `pyproject.toml`, `Makefile`).
  * **Detailed Breakdowns:** Expands on the contents of key directories like `docs` (SPARC phases, guides), `src` (modules: core, database, llm, rag, validation, ui, utils), `tests` (unit, integration, e2e, fixtures), `config` (base, environments), `scripts` (setup, maintenance, dev, deployment), and `data` (vector DB, schemas, logs).
  * **Documentation Focus:** Emphasizes `README.md` files within each major directory to explain its purpose and usage.
  * **Examples:** Includes templates for module READMEs, documentation index, project README, Makefile tasks, and `pyproject.toml`.
  * **Best Practices:** Adheres to principles like separation of concerns, modularity, discoverability, and environment separation.

-----

### Assumptions (`6_Assumptions_Requirements.md`)

This document explicitly lists the **underlying beliefs, dependencies, and expectations** influencing the project design, highlighting potential risks if these assumptions prove incorrect. It covers:

  * **Technical Infrastructure (A-1):** Assumes adequate hardware (16GB RAM, 8 cores), local DB access, reliable Ollama service, and acceptable CPU-only inference performance.
  * **User Behavior (A-2):** Assumes users have limited SQL knowledge but understand domain terms, accept 3-5s response times, and prefer conversational follow-ups.
  * **Data & Database (A-3):** Assumes a relatively stable schema, reasonable data quality, read-only access is sufficient, and sufficient sample data exists.
  * **Organizational Context (A-4):** Assumes HIPAA compliance is required, IT supports open-source tools, users primarily use desktops, and single-database support is sufficient initially.
  * **Resource Availability (A-5):** Assumes a dedicated team, access to SMEs, and budget for resources.
  * **Security & Compliance (A-6):** Assumes existing network security, SSO availability, and logging infrastructure.
  * **Integration & Dependencies (A-7):** Assumes temporary internet for model downloads, no external API dependencies post-setup, and Python ecosystem stability.
  * **Performance & Scale (A-8):** Assumes max 10-20 concurrent users, \<1000 DB tables, and \<10k rows per query result.
    Each assumption includes justification, impact, risk assessment, validation method, mitigation strategy, owner, and priority.

-----

### Architecture (`Architecture_Requirements.md`)

This document defines the **technical blueprint and high-level design** for the application, translating requirements into a concrete system structure. Key decisions and components include:

  * **Architectural Style:** **Modular Monolith** selected for balance of simplicity, modularity, performance, and compliance ease, rejecting microservices and traditional monoliths.
  * **Technology Stack:** Python 3.9+, Ollama (local LLM), ChromaDB (embedded vector store), pyodbc/SQLAlchemy (DB connector), Streamlit (MVP UI, FastAPI potential future), sentence-transformers (embeddings).
  * **Core Modules:** Defines distinct modules (`core`, `database`, `llm`, `rag`, `validation`, `ui`) with clear responsibilities and interfaces, enabling separation of concerns.
  * **Diagrams:** Includes System Context, Detailed Component Architecture, and Data Flow diagrams to visualize the structure and interactions.
  * **Data Models:** Specifies key data structures (e.g., `UserQuery`, `GeneratedSQL`, `QueryResult`, `SchemaElement`) using Python dataclasses.
  * **Key Components Deep Dive:** Provides detailed logic outlines for `QueryProcessor` (orchestrator), `RAGEngine` (retrieval), `LLMEngine` (generation), and `QueryValidator` (safety).
  * **Scalability Strategy:** Outlines vertical scaling for Phase 1 and horizontal scaling for Phase 2.
  * **Security Architecture:** Describes a defense-in-depth approach with multiple validation layers and HIPAA mapping.
  * **Performance Optimization:** Details caching strategies, database optimizations, and LLM prompt/inference tuning.
  * **Integration Points:** Defines interactions with SQL Server, SSO, SIEM, and monitoring tools.
  * **Deployment Architecture:** Proposes single-server Docker Compose for MVP and HA/Kubernetes options for future scale.
  * **AI Utilization:** Documents how AI assisted in architectural decisions and code generation.

```
┌────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE (Streamlit)                 │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐  ┌───────────┐   │
│  │Query Input │  │Clarification│ │   Results    │  │  History  │   │
│  │ Component  │  │   Dialog    │ │   Display    │  │  Sidebar  │   │
│  └─────┬──────┘  └──────┬─────┘  └──────┬───────┘  └─────┬─────┘   │
│        │                │               │                │         │
│        └────────────────┼───────────────┼────────────────┘         │
│                         │               │                          │
└─────────────────────────┼───────────────┼──────────────────────────┘
                          │ (User Action) │ (Display)
                          ▼               ▲
┌──────────────────────────────────────────────────────────────────────┐
│                    QUERY PROCESSOR (Core Orchestrator)               │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  1. Input Validation & Intent Classification ─→ [AMBIGUITY CHECK] │
│  │  2. RAG Context Retrieval (Dynamic K) ←───────────┘            │  │
│  │  3. SQL Generation (with Retry Loop) ──┐                       │  │
│  │  4. SQL Validation (Short-circuit) ←───┘                       │  │
│  │  5. Query Cost Estimation ─→ (Warn User)                       │  │
│  │  6. Database Execution (with Circuit Breaker)                  │  │
│  │  7. Result Formatting & Caching                                │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
                          │ (Calls to Engines)
        ┌─────────────────┼──────────────────┬─────────────────┐
        │                 │                  │                 │
        ▼                 ▼                  ▼                 ▼
┌───────────── ┐   ┌─────────────┐    ┌─────────────┐   ┌─────────────┐
│  RAG Engine  │   │  LLM Engine │    │  Validation │   │  Database   │
│(Relationship-│   │ (Ollama     │    │   Engine    │   │   Engine    │
│    Aware)    │   │  Client)    │    │ (Security)  │   │ (Connection │
└──────┬────── ┘   └──────┬──────┘    └─────────────┘   │    Pool)    │
       │                  │                             └──────┬──────┘
       ▼                  ▼                                     ▼
┌─────────────┐   ┌─────────────┐                       ┌─────────────┐
│  ChromaDB   │   │   Ollama    │                       │ SQL Server  │
│(Vector Store)│  │(Local LLM)  │                       │ (Database)  │
└─────────────┘   └─────────────┘                       └─────────────┘

```

-----

### Completion Plan (`Completion_Document.md`)

This document outlines the **final steps required for production deployment**, focusing on testing, compliance, deployment procedures, documentation, and monitoring. It acts as a checklist for go-live readiness:

  * **Testing Strategy:** Details unit, integration, system, performance (Locust), security (SAST, DAST, Pen Test), and User Acceptance Testing (UAT) with specific targets (e.g., 80%+ coverage, P95 latency \< 3.5s simple queries).
  * **Compliance & QA:** Verifies NFR compliance (HIPAA, performance, reliability), details security audit checklist, and performance QA procedures.
  * **Deployment & Rollback:** Provides pre-deployment checklist, deployment strategy (Blue/Green or Rolling via Docker Compose), and a clear rollback plan with triggers and actions.
  * **Documentation & Support:** Lists required user guides, technical docs (architecture, runbooks), and training materials.
  * **Post-Deployment:** Defines monitoring strategy (Prometheus/Grafana dashboards, alerts), maintenance cadence (daily, weekly, monthly tasks), and feedback loop mechanisms.
  * **Final Review:** Includes a Go/No-Go checklist covering technical, product, compliance, and stakeholder approvals.
  * **Reflection:** Summarizes lessons learned, goal achievement, future enhancements, and effectiveness of the SPARC framework.
  * **Appendices:** Includes CI/CD gates, smoke test script, quick commands, and Definition of Done.

-----

## 🧩 Thematic Analysis: Achieving Project Goals

The specification documents work cohesively to define a system aimed at democratizing data access in healthcare via local, secure natural language querying. Here's how key themes are addressed across the documents:

1.  **Core Goal: Natural Language Querying**

      * **Functional Requirements (FR-1, FR-2):** Define the core input (NL) and output (SQL) transformation.
      * **User Scenarios (Scenarios 1, 5):** Illustrate how users interact conversationally.
      * **UI/UX:** Specifies the input components and clear presentation of results.
      * **Architecture:** Details the `QueryProcessor`, `LLMEngine`, and data flow for this transformation.
      * **Assumptions (A-2.1, A-2.2):** Explicitly state the target user (non-SQL, domain expert).

2.  **Key Technology: Local LLM (Ollama) & RAG**

      * **Architecture:** Justifies Ollama for local processing (privacy) and ChromaDB (simplicity); details `LLMEngine` and `RAGEngine`.
      * **Functional Requirements (FR-3, FR-4):** Define RAG retrieval steps and LLM prompt construction/interaction.
      * **Non-Functional Requirements (NFR-1.2, NFR-1.4):** Set performance targets for LLM inference and vector search.
      * **Assumptions (A-1.3, A-7.2):** Confirm Ollama reliability and mandate no external API calls.
      * **File Structure:** Dedicates `src/llm` and `src/rag` modules.

3.  **Critical Constraint: Security & HIPAA Compliance**

      * **Non-Functional Requirements (NFR-2):** The primary driver, mandating local processing, encryption, audit logs, RBAC, etc.
      * **Architecture:** Implements defense-in-depth, maps features to HIPAA sections.
      * **Functional Requirements (FR-5, FR-12):** Detail validation layers (preventing injection/modification) and audit logging requirements.
      * **Assumptions (A-4.1, A-6.1, A-6.3):** Confirm HIPAA applicability and reliance on existing security infrastructure.
      * **Completion Plan:** Includes security testing (Pen Test) and audit verification.

4.  **User Experience & Usability**

      * **UI/UX Requirements:** Defines principles (clarity, consistency) and standards (WCAG AA).
      * **User Scenarios:** Drive design by showing real workflows, including errors and onboarding.
      * **Functional Requirements (FR-8, FR-9, FR-10, FR-11):** Specify conversational context, clear results, intuitive components, and helpful examples.
      * **Non-Functional Requirements (NFR-6):** Sets measurable usability targets (SUS score, learnability time).
      * **Assumptions (A-2.3, A-2.4):** Validate user expectations regarding response time and interaction style.

5.  **System Design & Implementation**

      * **Architecture:** Selects Modular Monolith, Python stack, defines components and data flow.
      * **File Structure:** Organizes code logically for maintainability.
      * **Functional/Non-Functional Requirements:** Provide the detailed "what" and "how well."
      * **Assumptions:** Document dependencies and potential risks impacting design.
      * **Completion Plan:** Guides testing, deployment, and monitoring based on the design.

6.  **Validation & Reliability**

      * **Functional Requirements (FR-5):** Defines multiple SQL safety check layers.
      * **Non-Functional Requirements (NFR-3):** Sets uptime targets and fault tolerance strategies.
      * **User Scenarios (Scenario 3):** Shows error recovery flow.
      * **Architecture:** Includes a dedicated `validation` module.
      * **Completion Plan:** Mandates extensive testing (unit, integration, E2E, load, security, UAT) before release.

These themes demonstrate a consistent focus across all specification documents, ensuring that the final system aligns with the core goals of providing secure, accurate, user-friendly, and locally processed natural language access to SQL databases within a healthcare context. The SPARC methodology ensures these aspects are considered systematically from initial requirements through to deployment planning.
