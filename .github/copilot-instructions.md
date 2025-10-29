## Purpose

This file gives concise, actionable guidance for an AI coding agent working in this repository (SQL_RAG).
Use it to understand the big-picture architecture, the project's expected patterns, and where to make minimally invasive edits.

## Where to read first

- `SPARC_Documents/SQL LLM RAG Project SPARC.md` — architecture overview, prompt patterns, and component responsibilities.
- `SPARC_Documents/Functional Requirements.md` — detailed functional requirements, RAG expectations, prompt assembly, and safety/validation rules.
- `README.md` — short repository summary.

## Big-picture architecture (from the SPARC docs)

- Major components: Vector Store (Chroma/FAISS), LLM layer (Ollama local models), Database interface (SQL Server via pyodbc/pymssql), and a Query Processing pipeline (retrieve → prompt → generate → validate → execute → format).
- Data flows: user NL → RAG retrieval (schema/examples) → prompt assembly → Ollama LLM → SQL extraction → validator (block write/DDL) → execute (read-only) → return results + store example back into vector DB.
- Why: system is designed to run locally (Ollama) for privacy and deterministic SQL generation (low temperature, few-shot examples). See the prompt engineering and validation sections in `SPARC_Documents/SQL LLM RAG Project SPARC.md`.

## Project-specific conventions and patterns

- Use Ollama for local LLM inference; prefer models listed in the SPARC doc (e.g., CodeLlama variants, SQLCoder) and low temperature (0.1) for deterministic SQL.
- RAG context must be limited to fit token budgets: prefer 3–5 schema/examples and deduplicate similar context pieces (see FR-3 in `Functional Requirements.md`).
- All generated SQL must be validated before execution. The docs show the exact prohibition list (DROP, DELETE, UPDATE, INSERT, TRUNCATE, DDL/DCL, system procedures) — implement checks as in the pseudocode `validate_sql` in the SPARC doc.
- Prefer CTEs for readability when generating nested/subquery logic. If JOINs exceed 5 tables or nesting >3, request clarification rather than auto-generate.

## Integration points & dependencies (discoverable in docs)

- Local LLM: Ollama (REST or Python client). Keep network calls to a local Ollama instance; the architecture assumes local models.
- Vector DB: Chroma or FAISS (local). Store schema fragments, example NL→SQL pairs, and business rules.
- Database: SQL Server (T-SQL). Use pyodbc/pymssql and a read-only user. All queries must be T-SQL compatible (square-bracket identifiers, GETDATE(), DATEADD(), etc.).

## Helpful examples (copy/paste-safe)

- Prompt template pattern (from SPARC doc):

```text
System instruction → Schema context → Few-shot examples → User question
Return ONLY the SQL query (no explanation)
```

- Safety check (prohibited keywords) — concept present in docs, use case-insensitive check for any of: DROP, DELETE, UPDATE, INSERT, TRUNCATE, ALTER, CREATE, GRANT, REVOKE, xp_cmdshell, sp_executesql.

## Developer workflows (quick reference)

- The project is Python-first in the SPARC docs. Typical local setup (PowerShell example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt   # if present; otherwise install langchain, chromadb, ollama client, pyodbc
```

- Ollama: install and pull model(s) locally per Ollama docs. Run the Ollama daemon locally before calling the Python client.
- Schema ingestion: follow `ingest_schema` pseudocode in `SQL LLM RAG Project SPARC.md` — query INFORMATION_SCHEMA, create embeddings, store them in the vector DB.

## Editing guidance for the AI agent

- Keep changes minimal and focused: update or add modules under `src/` (schema_loader, vector_store, llm_client, query_engine) as described in the SPARC doc structure.
- When adding prompts/templates, store them in a `config/` or `prompts/` directory and add a short README explaining variables and token budget expectations.
- Tests: add unit tests for `validate_sql` (check prohibited keywords, missing tables) and for prompt assembly (ensure token length limits and example inclusion). Place tests under `tests/`.

## What to avoid

- Do not default to remote/public LLM APIs; the design intentionally targets local Ollama models.
- Never run or deploy generation that allows DML/DDL without explicit, documented override and manual review.

## Where to add more guidance

- If you update behavior (e.g., new models, vector DB changes), add a short note in this file with one-line rationale and link to the edited doc/file.

---
If anything above is unclear or you want me to expand a section (examples, test templates, or a sample `requirements.txt`), tell me which part to iterate on.
