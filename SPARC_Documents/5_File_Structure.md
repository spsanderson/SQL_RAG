# **File Structure Proposal: Local LLM RAG SQL Query Application**

---

[Back to Main SPARC Documentation](SQL%20LLM%20RAG%20Project%20SPARC.md)

## **Overview**

This file structure proposal follows industry best practices for Python applications, emphasizing modularity, maintainability, and clear separation of concerns. The structure supports the SPARC methodology (Specification, Pseudocode, Architecture, Refinement, Completion) and enables efficient development, testing, and deployment.

**Design Principles**:

- **Separation of Concerns**: Code organized by functional domain
- **Scalability**: Easy to add new features without restructuring
- **Discoverability**: Intuitive naming and logical hierarchy
- **Documentation-First**: Markdown guides at every level
- **Environment Separation**: Clear distinction between dev, test, and prod

---

## **1. Root Directory Structure**

```
sql-rag-ollama/
│
├── .github/                      # GitHub-specific files
│   ├── workflows/                # CI/CD pipelines
│   │   ├── ci.yml               # Continuous integration
│   │   ├── deploy.yml           # Deployment automation
│   │   └── security-scan.yml    # Security scanning
│   ├── ISSUE_TEMPLATE/          # Issue templates
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── question.md
│   ├── PULL_REQUEST_TEMPLATE.md # PR template
│   └── CODEOWNERS               # Code ownership rules
│
├── docs/                         # Project documentation
│   ├── README.md                # Documentation index
│   ├── specification/           # SPARC: Specification phase
│   ├── architecture/            # SPARC: Architecture phase
│   ├── guides/                  # User and developer guides
│   ├── api/                     # API documentation
│   └── assets/                  # Images, diagrams, videos
│
├── src/                          # Application source code
│   ├── __init__.py
│   ├── main.py                  # Application entry point
│   ├── core/                    # Core business logic
│   ├── database/                # Database operations
│   ├── llm/                     # LLM integration
│   ├── rag/                     # RAG components
│   ├── validation/              # Validation logic
│   ├── ui/                      # User interface
│   └── utils/                   # Shared utilities
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   ├── e2e/                     # End-to-end tests
│   ├── fixtures/                # Test data and fixtures
│   ├── conftest.py              # Pytest configuration
│   └── README.md                # Testing guide
│
├── config/                       # Configuration files
│   ├── README.md                # Configuration guide
│   ├── database.yaml            # Database settings
│   ├── ollama.yaml              # LLM configuration
│   ├── rag.yaml                 # RAG settings
│   ├── security.yaml            # Security policies
│   ├── logging.yaml             # Logging configuration
│   └── environments/            # Environment-specific configs
│       ├── development.yaml
│       ├── staging.yaml
│       └── production.yaml
│
├── data/                         # Data storage (gitignored)
│   ├── README.md                # Data management guide
│   ├── vector_db/               # ChromaDB persistence
│   ├── schemas/                 # Cached database schemas
│   ├── example_queries/         # Example query library
│   ├── query_history/           # Historical queries
│   └── exports/                 # User-generated exports
│
├── scripts/                      # Utility scripts
│   ├── README.md                # Scripts usage guide
│   ├── setup/                   # Setup and installation
│   │   ├── install_dependencies.sh
│   │   ├── setup_database.py
│   │   └── init_vector_store.py
│   ├── maintenance/             # Maintenance tasks
│   │   ├── schema_refresh.py
│   │   ├── backup_data.sh
│   │   └── cleanup_logs.py
│   ├── development/             # Development utilities
│   │   ├── seed_data.py
│   │   ├── generate_examples.py
│   │   └── mock_database.py
│   └── deployment/              # Deployment scripts
│       ├── deploy.sh
│       ├── health_check.py
│       └── rollback.sh
│
├── monitoring/                   # Observability configuration
│   ├── README.md                # Monitoring guide
│   ├── prometheus/              # Prometheus configuration
│   │   ├── prometheus.yml
│   │   └── alerts.yml
│   ├── grafana/                 # Grafana dashboards
│   │   ├── dashboard.json
│   │   └── datasources.yml
│   └── logs/                    # Log aggregation config
│       └── logstash.conf
│
├── deployment/                   # Deployment configurations
│   ├── README.md                # Deployment guide
│   ├── docker/                  # Docker configuration
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   └── .dockerignore
│   ├── kubernetes/              # Kubernetes manifests
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── secrets.yaml
│   └── systemd/                 # Systemd service files
│       └── sql-rag-ollama.service
│
├── migrations/                   # Database migrations
│   ├── README.md                # Migration guide
│   ├── versions/                # Migration versions
│   └── alembic.ini              # Alembic configuration
│
├── .vscode/                      # VS Code workspace settings
│   ├── settings.json            # Editor settings
│   ├── launch.json              # Debug configurations
│   ├── extensions.json          # Recommended extensions
│   └── tasks.json               # Build tasks
│
├── .env.example                  # Environment variables template
├── .env.development              # Development environment vars
├── .env.test                     # Test environment vars
├── .gitignore                    # Git ignore rules
├── .dockerignore                 # Docker ignore rules
├── .pylintrc                     # Pylint configuration
├── .pre-commit-config.yaml       # Pre-commit hooks
│
├── pyproject.toml                # Project metadata (PEP 518)
├── setup.py                      # Package installation script
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── requirements-test.txt         # Testing dependencies
│
├── Makefile                      # Common tasks automation
├── README.md                     # Project overview
├── CHANGELOG.md                  # Version history
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                       # Software license
└── CODE_OF_CONDUCT.md            # Community guidelines
```

---

## **2. Detailed Directory Breakdown**

### **2.1 Documentation Structure (`/docs/`)**

```
docs/
│
├── README.md                     # Documentation index and navigation
│
├── specification/                # SPARC Phase 1: Specification
│   ├── 01_SPECIFICATION.md      # Main specification document
│   ├── 02_FUNCTIONAL_REQUIREMENTS.md
│   ├── 03_NON_FUNCTIONAL_REQUIREMENTS.md
│   ├── 04_USER_SCENARIOS.md
│   ├── 05_UI_UX_CONSIDERATIONS.md
│   ├── 06_DATA_MODELS.md
│   └── TEMPLATE_SPECIFICATION.md # Template for new specs
│
├── architecture/                 # SPARC Phase 3: Architecture
│   ├── 01_SYSTEM_OVERVIEW.md    # High-level architecture
│   ├── 02_COMPONENT_DESIGN.md   # Detailed component design
│   ├── 03_DATA_FLOW.md          # Data flow diagrams
│   ├── 04_INTEGRATION_POINTS.md # External integrations
│   ├── 05_SECURITY_ARCHITECTURE.md
│   ├── 06_DEPLOYMENT_ARCHITECTURE.md
│   └── diagrams/                # Architecture diagrams
│       ├── system_context.png
│       ├── component_diagram.png
│       ├── data_flow.png
│       └── deployment.png
│
├── guides/                       # User and developer guides
│   ├── user/                    # End-user documentation
│   │   ├── 01_GETTING_STARTED.md
│   │   ├── 02_BASIC_QUERIES.md
│   │   ├── 03_ADVANCED_FEATURES.md
│   │   ├── 04_QUERY_PATTERNS.md
│   │   ├── 05_EXPORTING_DATA.md
│   │   ├── 06_TROUBLESHOOTING.md
│   │   └── FAQ.md
│   │
│   ├── developer/               # Developer documentation
│   │   ├── 01_SETUP.md          # Development environment setup
│   │   ├── 02_ARCHITECTURE_OVERVIEW.md
│   │   ├── 03_CODING_STANDARDS.md
│   │   ├── 04_TESTING_GUIDE.md
│   │   ├── 05_CONTRIBUTION_WORKFLOW.md
│   │   ├── 06_DEBUGGING.md
│   │   └── 07_DEPLOYMENT.md
│   │
│   └── admin/                   # System administrator guide
│       ├── 01_INSTALLATION.md
│       ├── 02_CONFIGURATION.md
│       ├── 03_MONITORING.md
│       ├── 04_BACKUP_RECOVERY.md
│       ├── 05_TROUBLESHOOTING.md
│       └── 06_SECURITY.md
│
├── api/                          # API documentation
│   ├── README.md                # API overview
│   ├── rest_api.md              # REST API reference
│   ├── websocket_api.md         # WebSocket API reference
│   ├── internal_api.md          # Internal module APIs
│   └── examples/                # API usage examples
│       ├── python_examples.py
│       └── curl_examples.sh
│
├── decisions/                    # Architecture Decision Records
│   ├── README.md                # ADR index
│   ├── 001_use_ollama.md
│   ├── 002_chromadb_vector_store.md
│   ├── 003_sqlcoder_model_choice.md
│   ├── 004_streamlit_vs_flask.md
│   └── TEMPLATE_ADR.md          # ADR template
│
├── runbooks/                     # Operational runbooks
│   ├── incident_response.md
│   ├── schema_refresh.md
│   ├── performance_tuning.md
│   └── disaster_recovery.md
│
└── assets/                       # Documentation assets
    ├── images/                  # Screenshots, diagrams
    ├── videos/                  # Tutorial videos
    └── templates/               # Document templates
```

**Key Documentation Files**:

#### **`docs/README.md`** - Documentation Index

```markdown
# SQL RAG Ollama Documentation

Welcome to the SQL RAG Ollama documentation. This guide will help you understand, use, and contribute to the project.

## 📚 Documentation Structure

### For Users
- [Getting Started Guide](guides/user/01_GETTING_STARTED.md) - First steps
- [Basic Queries](guides/user/02_BASIC_QUERIES.md) - Query basics
- [Advanced Features](guides/user/03_ADVANCED_FEATURES.md) - Power user features
- [FAQ](guides/user/FAQ.md) - Common questions

### For Developers
- [Development Setup](guides/developer/01_SETUP.md) - Environment setup
- [Architecture Overview](guides/developer/02_ARCHITECTURE_OVERVIEW.md)
- [Coding Standards](guides/developer/03_CODING_STANDARDS.md)
- [Testing Guide](guides/developer/04_TESTING_GUIDE.md)

### For Administrators
- [Installation Guide](guides/admin/01_INSTALLATION.md)
- [Configuration](guides/admin/02_CONFIGURATION.md)
- [Monitoring](guides/admin/03_MONITORING.md)

## 🏗️ SPARC Methodology

This project follows the SPARC framework:
1. [Specification](specification/01_SPECIFICATION.md) - Requirements and design
2. Pseudocode - Algorithm design (in code comments)
3. [Architecture](architecture/01_SYSTEM_OVERVIEW.md) - System design
4. Refinement - Iterative improvement
5. Completion - Final implementation

## 📖 Additional Resources

- [API Reference](api/README.md)
- [Architecture Decisions](decisions/README.md)
- [Operational Runbooks](runbooks/)

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.
```

---

### **2.2 Source Code Structure (`/src/`)**

```
src/
│
├── __init__.py                   # Package initialization
├── main.py                       # Application entry point
├── config_loader.py              # Configuration management
│
├── core/                         # Core business logic
│   ├── __init__.py
│   ├── README.md                # Core module overview
│   ├── query_processor.py       # Main query orchestration
│   ├── intent_classifier.py     # Natural language intent parsing
│   ├── conversation_manager.py  # Session and context management
│   ├── query_optimizer.py       # Query optimization logic
│   └── exceptions.py            # Custom exception classes
│
├── database/                     # Database operations
│   ├── __init__.py
│   ├── README.md                # Database module overview
│   ├── connection.py            # Connection management
│   ├── connection_pool.py       # Connection pooling
│   ├── schema_loader.py         # Schema extraction
│   ├── query_executor.py        # SQL execution
│   ├── result_formatter.py      # Result formatting
│   ├── adapters/                # Database-specific adapters
│   │   ├── __init__.py
│   │   ├── base_adapter.py     # Abstract base adapter
│   │   ├── sqlserver_adapter.py
│   │   ├── postgres_adapter.py # Future support
│   │   └── mysql_adapter.py    # Future support
│   └── models.py                # Database ORM models
│
├── llm/                          # LLM integration
│   ├── __init__.py
│   ├── README.md                # LLM module overview
│   ├── ollama_client.py         # Ollama API client
│   ├── prompt_builder.py        # Prompt construction
│   ├── prompt_templates.py      # Prompt templates
│   ├── sql_parser.py            # SQL extraction from LLM
│   ├── model_manager.py         # Model loading/switching
│   ├── context_manager.py       # LLM context management
│   └── retry_logic.py           # Retry strategies
│
├── rag/                          # RAG components
│   ├── __init__.py
│   ├── README.md                # RAG module overview
│   ├── vector_store.py          # ChromaDB interface
│   ├── embeddings.py            # Embedding generation
│   ├── retriever.py             # Context retrieval
│   ├── indexer.py               # Document indexing
│   ├── schema_embedder.py       # Schema embedding
│   ├── query_embedder.py        # Query embedding
│   └── similarity.py            # Similarity calculations
│
├── validation/                   # Validation and safety
│   ├── __init__.py
│   ├── README.md                # Validation module overview
│   ├── sql_validator.py         # SQL safety checks
│   ├── schema_validator.py      # Schema validation
│   ├── input_sanitizer.py       # Input sanitization
│   ├── query_analyzer.py        # Query complexity analysis
│   ├── security_rules.py        # Security policy enforcement
│   └── validators/              # Specific validators
│       ├── __init__.py
│       ├── injection_validator.py
│       ├── permission_validator.py
│       └── complexity_validator.py
│
├── ui/                           # User interface
│   ├── __init__.py
│   ├── README.md                # UI module overview
│   ├── app.py                   # Main UI application
│   ├── streamlit_app.py         # Streamlit implementation
│   ├── components/              # Reusable UI components
│   │   ├── __init__.py
│   │   ├── query_input.py
│   │   ├── result_display.py
│   │   ├── history_sidebar.py
│   │   ├── schema_browser.py
│   │   ├── export_buttons.py
│   │   └── loading_states.py
│   ├── pages/                   # Multi-page app pages
│   │   ├── home.py
│   │   ├── admin.py
│   │   └── settings.py
│   ├── styles/                  # CSS and styling
│   │   ├── main.css
│   │   ├── components.css
│   │   └── themes.css
│   └── static/                  # Static assets
│       ├── images/
│       ├── icons/
│       └── fonts/
│
├── utils/                        # Shared utilities
│   ├── __init__.py
│   ├── README.md                # Utils module overview
│   ├── logger.py                # Logging configuration
│   ├── date_parser.py           # Natural date parsing
│   ├── metrics.py               # Performance metrics
│   ├── cache.py                 # Caching utilities
│   ├── formatters.py            # Data formatting
│   ├── validators.py            # General validators
│   └── helpers.py               # Helper functions
│
└── api/                          # API endpoints (if REST API)
    ├── __init__.py
    ├── README.md                # API module overview
    ├── routes/                  # API route definitions
    │   ├── __init__.py
    │   ├── query.py
    │   ├── history.py
    │   └── admin.py
    ├── middleware/              # API middleware
    │   ├── auth.py
    │   ├── rate_limit.py
    │   └── error_handler.py
    └── schemas/                 # API request/response schemas
        ├── query_schema.py
        ├── response_schema.py
        └── error_schema.py
```

**Module README Template** (`src/[module]/README.md`):

```markdown
# [Module Name] Module

## Purpose
Brief description of what this module does and its role in the application.

## Components

### [Component Name]
- **File**: `component_file.py`
- **Purpose**: What it does
- **Key Functions**:
  - `function_name()` - Description
  - `another_function()` - Description
- **Dependencies**: Other modules it depends on
- **Usage Example**:

  ``python
  from src.module import Component
  component = Component()
  result = component.do_something()
  ``

```

## Architecture

[Brief architecture diagram or description]

## Configuration

Configuration options specific to this module (reference config files).

## Testing

How to test this module:

```bash
pytest tests/unit/module/
```

## Contributing

Guidelines specific to this module.

---

### **2.3 Test Structure (`/tests/`)**

```
tests/
│
├── __init__.py
├── README.md                     # Testing guide and standards
├── conftest.py                   # Pytest configuration and fixtures
│
├── unit/                         # Unit tests (isolated components)
│   ├── __init__.py
│   ├── test_query_processor.py
│   ├── test_sql_validator.py
│   ├── test_prompt_builder.py
│   ├── test_rag_retriever.py
│   ├── test_schema_loader.py
│   ├── database/                # Database unit tests
│   │   ├── test_connection.py
│   │   ├── test_query_executor.py
│   │   └── test_result_formatter.py
│   ├── llm/                     # LLM unit tests
│   │   ├── test_ollama_client.py
│   │   └── test_sql_parser.py
│   └── validation/              # Validation unit tests
│       ├── test_sql_validator.py
│       └── test_input_sanitizer.py
│
├── integration/                  # Integration tests (multiple components)
│   ├── __init__.py
│   ├── test_end_to_end_query.py
│   ├── test_rag_pipeline.py
│   ├── test_database_integration.py
│   ├── test_llm_integration.py
│   └── test_ui_backend_integration.py
│
├── e2e/                          # End-to-end tests (full system)
│   ├── __init__.py
│   ├── test_user_workflows.py   # User scenario tests
│   ├── test_query_scenarios.py
│   ├── test_error_recovery.py
│   └── test_performance.py
│
├── fixtures/                     # Test data and fixtures
│   ├── __init__.py
│   ├── sample_queries.json      # Example queries
│   ├── mock_schema.json         # Mock database schema
│   ├── expected_sql.json        # Expected SQL outputs
│   ├── mock_responses.json      # Mock LLM responses
│   └── test_data.sql            # Test database data
│
├── mocks/                        # Mock objects and stubs
│   ├── __init__.py
│   ├── mock_database.py         # Mock database connection
│   ├── mock_ollama.py           # Mock Ollama client
│   ├── mock_vector_store.py     # Mock vector store
│   └── mock_ui.py               # Mock UI components
│
├── benchmarks/                   # Performance benchmarks
│   ├── __init__.py
│   ├── benchmark_query_processing.py
│   ├── benchmark_llm_inference.py
│   ├── benchmark_rag_retrieval.py
│   └── benchmark_results.json
│
├── load/                         # Load testing
│   ├── locustfile.py            # Locust load test scenarios
│   ├── load_test_config.yaml
│   └── results/                 # Load test results
│
└── security/                     # Security tests
    ├── test_sql_injection.py
    ├── test_authentication.py
    ├── test_authorization.py
    └── test_input_validation.py
```

**Testing README** (`tests/README.md`):

```markdown
# Testing Guide

## Test Structure

- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test multiple components working together
- **E2E Tests**: Test complete user workflows
- **Load Tests**: Test system under load
- **Security Tests**: Test security vulnerabilities

## Running Tests

```bash
# All tests
make test

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# E2E tests
pytest tests/e2e/

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/unit/test_query_processor.py

# Specific test function
pytest tests/unit/test_query_processor.py::test_simple_query
```

## Writing Tests

### Unit Test Example

```python
def test_sql_validator_blocks_drop():
    validator = SQLValidator()
    sql = "DROP TABLE users;"
  
    with pytest.raises(SecurityError):
        validator.validate(sql)
```

### Integration Test Example

```python
def test_query_processing_pipeline():
    processor = QueryProcessor()
    query = "How many patients admitted yesterday?"
  
    result = processor.process(query)
  
    assert result.success is True
    assert result.row_count > 0
```

## Test Coverage Goals

- **Overall Coverage**: ≥ 80%
- **Core Modules**: ≥ 90%
- **Validation**: 100%

## CI/CD Integration

Tests run automatically on:

- Every push to main
- Every pull request
- Nightly builds

See `.github/workflows/ci.yml` for details.

---

### **2.4 Configuration Structure (`/config/`)**

```

config/
│
├── README.md                     # Configuration guide
│
├── database.yaml                 # Database configuration
├── ollama.yaml                   # LLM configuration
├── rag.yaml                      # RAG configuration
├── security.yaml                 # Security policies
├── logging.yaml                  # Logging configuration
├── monitoring.yaml               # Monitoring configuration
├── ui.yaml                       # UI configuration
│
├── environments/                 # Environment-specific configs
│   ├── development.yaml         # Dev environment
│   ├── staging.yaml             # Staging environment
│   └── production.yaml          # Production environment
│
├── templates/                    # Configuration templates
│   ├── database.template.yaml
│   └── ollama.template.yaml
│
└── schemas/                      # Configuration schemas (validation)
    ├── database_schema.json
    └── ollama_schema.json

```

**Example Configuration Files**:

#### **`config/database.yaml`**
```yaml
# Database Configuration
database:
  sql_server:
    # Connection settings
    host: ${DB_HOST:localhost}
    port: ${DB_PORT:1433}
    database: ${DB_NAME:production}
    username: ${DB_USER:readonly_user}
    password: ${DB_PASSWORD}  # From environment variable
  
    # Connection pool settings
    connection_pool:
      min_size: 5
      max_size: 20
      timeout: 30  # seconds
      max_overflow: 10
      pool_recycle: 3600  # 1 hour
  
    # Query settings
    query:
      timeout: 30  # seconds
      max_rows: 10000
      default_limit: 1000
  
    # Schema management
    schema:
      refresh_interval: 86400  # 24 hours (seconds)
      cache_enabled: true
      cache_ttl: 3600  # 1 hour
    
  # Future database support
  postgresql:
    enabled: false
  mysql:
    enabled: false
```

#### **`config/ollama.yaml`**

```yaml
# Ollama LLM Configuration
ollama:
  # Connection settings
  base_url: http://localhost:11434
  timeout: 45  # seconds
  
  # Model settings
  model:
    name: sqlcoder:7b-q4
    alternative: codellama:7b
  
    # Generation parameters
    temperature: 0.1  # Low for deterministic SQL
    top_p: 0.9
    top_k: 40
    max_tokens: 512
    stop_sequences:
      - ";"
      - "```"
  
  # Performance settings
  performance:
    num_ctx: 2048  # Context window
    num_thread: 8  # CPU threads
    use_mmap: true
    use_mlock: false
  
  # Retry logic
  retry:
    max_attempts: 3
    backoff_factor: 2
    timeout_multiplier: 1.5
```

#### **`config/rag.yaml`**

```yaml
# RAG Configuration
rag:
  # Vector store settings
  vector_store:
    provider: chromadb
    persist_directory: ./data/vector_db
    collection_name: sql_schema
  
    # Embedding settings
    embedding:
      model: all-MiniLM-L6-v2
      dimension: 384
      batch_size: 32
      normalize: true
  
    # Search settings
    search:
      top_k: 5
      similarity_threshold: 0.7
      search_type: similarity  # or mmr
      fetch_k: 20  # for MMR
      lambda_mult: 0.5  # for MMR diversity
  
  # Context retrieval
  retrieval:
    max_context_tokens: 2000
    include_examples: true
    include_business_rules: true
    prioritize_recent: true
  
  # Indexing settings
  indexing:
    batch_size: 100
    chunk_size: 512
    chunk_overlap: 50
```

**Configuration README** (`config/README.md`):

```markdown
# Configuration Guide

## Overview

All configuration is externalized using YAML files and environment variables.

## Configuration Files

- `database.yaml` - Database connection and settings
- `ollama.yaml` - LLM model and inference settings
- `rag.yaml` - Vector store and retrieval settings
- `security.yaml` - Security policies
- `logging.yaml` - Logging configuration

## Environment Variables

Sensitive values use environment variables with syntax: `${VAR_NAME:default}`

Required environment variables:
```bash
DB_HOST=localhost
DB_PORT=1433
DB_NAME=production
DB_USER=readonly_user
DB_PASSWORD=secure_password
```

## Environment-Specific Configurations

Override defaults with environment-specific files:

- `environments/development.yaml`
- `environments/staging.yaml`
- `environments/production.yaml`

Load with:

```python
from src.config_loader import load_config
config = load_config(environment='production')
```

## Configuration Validation

Configurations are validated against JSON schemas in `schemas/`.

## Security

- Never commit `.env` files
- Never commit passwords or secrets
- Use secrets management (Vault, AWS Secrets Manager) in production
- Encrypt sensitive configuration files

## Examples

See `templates/` for configuration templates.

---

### **2.5 Scripts Structure (`/scripts/`)**

```

scripts/
│
├── README.md                     # Scripts usage guide
│
├── setup/                        # Setup and installation
│   ├── install_dependencies.sh  # Install Python packages
│   ├── install_ollama.sh        # Install Ollama
│   ├── setup_database.py        # Database initialization
│   ├── init_vector_store.py     # Initialize ChromaDB
│   └── configure_environment.sh # Environment setup
│
├── maintenance/                  # Maintenance tasks
│   ├── schema_refresh.py        # Refresh database schema
│   ├── backup_data.sh           # Backup vector store and data
│   ├── cleanup_logs.py          # Log cleanup
│   ├── vacuum_vector_store.py   # Vector store optimization
│   └── health_check.py          # System health check
│
├── development/                  # Development utilities
│   ├── seed_data.py             # Seed development data
│   ├── generate_examples.py     # Generate example queries
│   ├── mock_database.py         # Start mock database
│   ├── run_dev_server.sh        # Start development server
│   └── reset_dev_environment.sh # Reset dev environment
│
├── deployment/                   # Deployment scripts
│   ├── deploy.sh                # Deploy application
│   ├── deploy_docker.sh         # Docker deployment
│   ├── deploy_k8s.sh            # Kubernetes deployment
│   ├── health_check.py          # Post-deployment health check
│   ├── rollback.sh              # Rollback deployment
│   └── smoke_test.py            # Post-deployment smoke test
│
├── testing/                      # Testing utilities
│   ├── run_tests.sh             # Run test suite
│   ├── run_integration_tests.sh # Integration tests only
│   ├── generate_coverage.sh     # Generate coverage report
│   └── benchmark.py             # Run performance benchmarks
│
└── monitoring/                   # Monitoring utilities
    ├── export_metrics.py        # Export metrics
    ├── analyze_logs.py          # Log analysis
    └── generate_report.py       # Generate health report

```

**Example Script** - `scripts/setup/install_dependencies.sh`:
```bash
#!/bin/bash

# Install Dependencies Script
# This script installs all required dependencies for the SQL RAG Ollama application

set -e  # Exit on error

echo "=== SQL RAG Ollama - Dependency Installation ==="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python $required_version or higher is required"
    exit 1
fi

echo "✓ Python $python_version detected"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✓ Virtual environment created"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install production dependencies
echo "Installing production dependencies..."
pip install -r requirements.txt

echo "✓ Production dependencies installed"

# Install development dependencies (if in dev mode)
if [ "$1" == "--dev" ]; then
    echo "Installing development dependencies..."
    pip install -r requirements-dev.txt
    echo "✓ Development dependencies installed"
fi

# Install testing dependencies (if in test mode)
if [ "$1" == "--test" ] || [ "$1" == "--dev" ]; then
    echo "Installing testing dependencies..."
    pip install -r requirements-test.txt
    echo "✓ Testing dependencies installed"
fi

# Verify installations
echo "Verifying installations..."
pip check

echo ""
echo "=== Installation Complete ==="
echo "Activate the virtual environment with: source venv/bin/activate"
```

---

### **2.6 Data Directory Structure (`/data/`)**

```
data/                             # Data storage (gitignored)
│
├── README.md                     # Data management guide
├── .gitkeep                      # Keep directory in git
│
├── vector_db/                    # ChromaDB persistence
│   ├── chroma.sqlite3           # ChromaDB database
│   ├── index/                   # Vector indexes
│   └── backups/                 # Vector DB backups
│
├── schemas/                      # Cached database schemas
│   ├── current/                 # Current schema
│   │   ├── tables.json
│   │   ├── columns.json
│   │   └── relationships.json
│   ├── versions/                # Schema versions
│   │   ├── 2025-10-29_schema.json
│   │   └── 2025-10-28_schema.json
│   └── metadata.json            # Schema metadata
│
├── example_queries/              # Example query library
│   ├── operations/
│   │   ├── discharges.json
│   │   ├── census.json
│   │   └── admissions.json
│   ├── financial/
│   │   ├── revenue.json
│   │   └── charges.json
│   ├── quality/
│   │   ├── readmissions.json
│   │   └── patient_safety.json
│   └── index.json               # Query index
│
├── query_history/                # Historical queries
│   ├── 2025/
│   │   ├── 10/
│   │   │   ├── 29.jsonl        # Daily query log
│   │   │   └── 28.jsonl
│   │   └── archive/
│   └── index.db                 # Query history database
│
├── exports/                      # User-generated exports
│   ├── csv/
│   ├── excel/
│   └── json/
│
├── logs/                         # Application logs
│   ├── application.log
│   ├── query.log
│   ├── error.log
│   ├── security.log
│   └── archive/                 # Archived logs
│
├── cache/                        # Application cache
│   ├── query_results/
│   ├── schema_cache/
│   └── embedding_cache/
│
└── temp/                         # Temporary files
    └── processing/
```

**Data Management README** (`data/README.md`):

```markdown
# Data Directory

This directory contains application data, caches, and user-generated content.

## ⚠️ Important Notes

- **Gitignored**: This directory is not tracked by git (except this README)
- **Sensitive Data**: May contain query history and user data
- **Backup Required**: Regularly backup `vector_db/` and `query_history/`
- **Permissions**: Ensure proper file permissions (600 for sensitive files)

## Directory Structure

### `/vector_db/`
ChromaDB vector store for RAG retrieval. Contains embedded database schema and example queries.

**Backup**: Daily automated backup to `backups/`

### `/schemas/`
Cached database schema information. Refreshed daily.

**Files**:
- `current/` - Current schema in use
- `versions/` - Historical schema versions (30-day retention)

### `/example_queries/`
Curated example queries organized by category.

**Format**: JSON files with structure:
```json
{
  "category": "operations",
  "queries": [
    {
      "id": "discharge_count",
      "question": "How many patients discharged yesterday?",
      "sql": "SELECT COUNT(*) ...",
      "tags": ["discharge", "daily", "count"]
    }
  ]
}
```

### `/query_history/`

Historical query logs for analytics and learning.

**Format**: JSONL (one JSON object per line) for efficient appending
**Retention**: 90 days in hot storage, archived thereafter

### `/logs/`

Application logs. See `config/logging.yaml` for configuration.

**Rotation**: Daily, compressed after 7 days, retained for 90 days

### `/cache/`

Temporary cache for performance optimization.

**Eviction**: LRU policy, max 1GB

### `/exports/`

User-generated data exports.

**Cleanup**: Files older than 30 days automatically deleted

## Data Lifecycle

1. **Creation**: Data created during normal operation
2. **Usage**: Cached and retrieved as needed
3. **Archival**: Old data moved to archive after retention period
4. **Deletion**: Archived data deleted after compliance period

## Backup Strategy

### Daily Backups

```bash
scripts/maintenance/backup_data.sh
```

Backs up:

- Vector database
- Query history (last 30 days)
- Current schema

### Restore Process

```bash
scripts/maintenance/restore_data.sh <backup_file>
```

## Compliance

- Query history retained for 90 days (HIPAA requirement)
- Audit logs retained for 7 years
- PII/PHI never stored in query history (masked)

```

---

### **2.7 Root-Level Files**

#### **`README.md`** - Project Overview
```markdown
# SQL RAG Ollama - Natural Language Database Query System

Ask questions about your data in plain English. Get SQL and results back.

## 🎯 Quick Start

```bash
# Clone repository
git clone https://github.com/yourorg/sql-rag-ollama.git
cd sql-rag-ollama

# Run setup
./scripts/setup/install_dependencies.sh --dev
./scripts/setup/setup_database.py
./scripts/setup/init_vector_store.py

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Start application
python src/main.py
```

## 📖 Documentation

- [User Guide](docs/guides/user/01_GETTING_STARTED.md)
- [Developer Guide](docs/guides/developer/01_SETUP.md)
- [API Documentation](docs/api/README.md)
- [Architecture](docs/architecture/01_SYSTEM_OVERVIEW.md)

## 🏗️ Architecture

Built with:

- **Ollama** - Local LLM inference (SQLCoder-7B)
- **ChromaDB** - Vector database for RAG
- **Python 3.9+** - Application runtime
- **Streamlit** - Web UI

## 🧪 Testing

```bash
# All tests
make test

# Unit tests only
pytest tests/unit/

# With coverage
pytest --cov=src
```

## 📦 Project Structure

```
sql-rag-ollama/
├── src/           # Source code
├── tests/         # Test suite
├── docs/          # Documentation
├── config/        # Configuration
├── scripts/       # Utility scripts
└── data/          # Data storage
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

[MIT License](LICENSE)

## 🔗 Links

- [Documentation](https://docs.example.com)
- [Issue Tracker](https://github.com/yourorg/sql-rag-ollama/issues)
- [Discussions](https://github.com/yourorg/sql-rag-ollama/discussions)

```

#### **`Makefile`** - Task Automation
```makefile
# Makefile for SQL RAG Ollama

.PHONY: help setup test clean run deploy

# Default target
help:
	@echo "SQL RAG Ollama - Available Commands:"
	@echo ""
	@echo "  make setup       - Set up development environment"
	@echo "  make test        - Run test suite"
	@echo "  make test-unit   - Run unit tests only"
	@echo "  make test-cov    - Run tests with coverage"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code"
	@echo "  make clean       - Clean temporary files"
	@echo "  make run         - Run application"
	@echo "  make run-dev     - Run in development mode"
	@echo "  make docker      - Build Docker image"
	@echo "  make deploy      - Deploy to production"
	@echo "  make docs        - Generate documentation"

setup:
	@echo "Setting up development environment..."
	bash scripts/setup/install_dependencies.sh --dev
	bash scripts/setup/configure_environment.sh
	python scripts/setup/setup_database.py
	python scripts/setup/init_vector_store.py

test:
	@echo "Running test suite..."
	pytest tests/ -v

test-unit:
	@echo "Running unit tests..."
	pytest tests/unit/ -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:
	@echo "Running linters..."
	pylint src/
	ruff check src/
	mypy src/

format:
	@echo "Formatting code..."
	black src/ tests/
	isort src/ tests/

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf .coverage htmlcov
	rm -rf build/ dist/

run:
	@echo "Starting application..."
	python src/main.py

run-dev:
	@echo "Starting application in development mode..."
	ENVIRONMENT=development python src/main.py --reload

docker:
	@echo "Building Docker image..."
	docker build -t sql-rag-ollama:latest -f deployment/docker/Dockerfile .

docker-compose:
	@echo "Starting with Docker Compose..."
	docker-compose -f deployment/docker/docker-compose.yml up

deploy:
	@echo "Deploying to production..."
	bash scripts/deployment/deploy.sh

docs:
	@echo "Generating documentation..."
	sphinx-build -b html docs/ docs/_build/
```

#### **`pyproject.toml`** - Project Metadata

```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "sql-rag-ollama"
version = "0.1.0"
description = "Natural language interface for SQL databases using local LLMs"
authors = [
    {name = "Your Organization", email = "dev@example.com"}
]
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
keywords = ["sql", "llm", "rag", "ollama", "natural-language"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Healthcare Industry",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

dependencies = [
    "langchain>=0.1.0",
    "chromadb>=0.4.0",
    "ollama>=0.1.0",
    "streamlit>=1.28.0",
    "pandas>=2.0.0",
    "pyyaml>=6.0",
    "python-dotenv>=1.0.0",
    "pyodbc>=5.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "pylint>=3.0.0",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
]

test = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "faker>=20.0.0",
    "locust>=2.17.0",
]

[project.urls]
Homepage = "https://github.com/yourorg/sql-rag-ollama"
Documentation = "https://docs.example.com"
Repository = "https://github.com/yourorg/sql-rag-ollama"
"Bug Tracker" = "https://github.com/yourorg/sql-rag-ollama/issues"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests",
    "slow: Slow running tests",
]

[tool.black]
line-length = 100
target-version = ["py39", "py310", "py311"]
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.ruff]
line-length = 100
target-version = "py39"
select = ["E", "F", "W", "C", "N"]
```

---

## **3. Development Workflow Documentation**

### **`CONTRIBUTING.md`**

```markdown
# Contributing to SQL RAG Ollama

Thank you for your interest in contributing! This guide will help you get started.

## 📋 Prerequisites

- Python 3.9 or higher
- Git
- Ollama installed locally
- SQL Server access (or mock database)

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/sql-rag-ollama.git
   cd sql-rag-ollama
```

2. **Set up development environment**

   ```bash
   make setup
   source venv/bin/activate
   ```
3. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💻 Development Process

### Code Standards

- Follow PEP 8 style guide
- Write docstrings for all public functions (Google style)
- Add type hints to function signatures
- Keep functions under 50 lines
- Maintain test coverage above 80%

### Before Committing

```bash
# Format code
make format

# Run linters
make lint

# Run tests
make test

# Check coverage
make test-cov
```

### Commit Messages

Follow conventional commits format:

```
type(scope): subject

body

footer
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:

```
feat(llm): add retry logic for failed queries

Implement exponential backoff retry strategy for LLM
requests that fail due to temporary network issues.

Closes #123
```

## 🧪 Testing

- Write unit tests for new functions
- Add integration tests for new features
- Update E2E tests for user-facing changes
- Ensure all tests pass before submitting PR

## 📝 Documentation

- Update relevant documentation in `docs/`
- Add docstrings to new functions
- Update README if adding user-facing features
- Create ADR for architectural decisions

## 🔍 Code Review

All submissions require review. We use GitHub pull requests:

1. Push your changes to your fork
2. Create pull request to `main` branch
3. Fill out PR template completely
4. Address review feedback
5. Maintain clean commit history (squash if needed)

## 📦 Releases

Releases are managed by maintainers. Version follows SemVer.

## ❓ Questions

- GitHub Discussions for questions
- Issues for bug reports
- Pull requests for contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

```

---

## **4. Deployment Structure**

### **Docker Structure (`/deployment/docker/`)**

```

deployment/docker/
│
├── Dockerfile                    # Main application image
├── Dockerfile.ollama             # Ollama service image
├── docker-compose.yml            # Multi-container orchestration
├── docker-compose.dev.yml        # Development overrides
├── docker-compose.prod.yml       # Production configuration
├── .dockerignore                 # Docker ignore rules
│
└── scripts/
    ├── entrypoint.sh            # Container entrypoint
    ├── healthcheck.sh           # Health check script
    └── wait-for-it.sh           # Wait for services script

```

**`Dockerfile`**:
```dockerfile
# Multi-stage build for optimized image

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY src/ /app/src/
COPY config/ /app/config/
COPY scripts/ /app/scripts/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python scripts/maintenance/health_check.py

# Expose port
EXPOSE 8501

# Entry point
ENTRYPOINT ["python", "src/main.py"]
```

---

## **5. Summary: File Structure Best Practices**

### **Key Principles Applied**

1. **Modularity**: Each directory has a single, clear purpose
2. **Documentation**: README.md at every level explains purpose and usage
3. **Separation**: Config, code, tests, docs clearly separated
4. **Scalability**: Easy to add new modules without restructuring
5. **Standards**: Follows Python community conventions
6. **Discoverability**: Intuitive naming, logical hierarchy
7. **Automation**: Scripts for common tasks
8. **Environment Management**: Clear dev/test/prod separation

### **Navigation Guide**

```
Starting Point → Purpose
─────────────────────────────────────────────────────────
README.md       → Project overview, quick start
docs/           → All documentation
src/            → All application code
tests/          → All tests
config/         → All configuration
scripts/        → Automation and utilities
```

### **File Organization Rules**

✅ **DO**:

- Keep related files together
- Use descriptive directory names
- Include README.md in each major directory
- Follow consistent naming conventions
- Separate code from config from data
- Version control everything except data/

❌ **DON'T**:

- Mix concerns in single directory
- Use cryptic abbreviations
- Commit sensitive data or credentials
- Commit generated files (.pyc, __pycache__)
- Create deep nesting (> 4 levels)

This file structure provides a solid foundation for development, testing, deployment, and maintenance of the SQL RAG Ollama application while following SPARC methodology and industry best practices.
