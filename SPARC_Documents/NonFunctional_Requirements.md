# **Non-Functional Requirements: Local LLM RAG SQL Query Application**

---
[Back to Main SPARC Documentation](SQL%20LLM%20RAG%20Project%20SPARC.md)

## **Overview**

Non-functional requirements (NFRs) define how the system performs its functions, specifying quality attributes, constraints, and operational characteristics. These requirements are critical for user satisfaction, system reliability, and long-term viability. Each NFR includes measurable criteria, importance justification, and validation methods.

---

## **NFR-1: Performance Requirements**

**Category**: Performance | **Priority**: CRITICAL | **Impact**: High

### **Description**
The system must deliver fast response times and efficient resource utilization to ensure user productivity and satisfaction. Performance directly affects user adoption and perceived system quality.

---

### **NFR-1.1: Query Response Time**

**Importance**: Fast responses are essential for interactive workflows. Users abandon systems with slow response times, especially for simple queries that should feel instantaneous.

#### **Metrics and Targets**

| **Query Type** | **Target (95th percentile)** | **Maximum (99th percentile)** |
|----------------|------------------------------|-------------------------------|
| Simple SELECT (single table) | < 3 seconds | < 5 seconds |
| Complex JOIN (2-3 tables) | < 8 seconds | < 12 seconds |
| Aggregation queries | < 5 seconds | < 8 seconds |
| Multi-hop JOINs (4+ tables) | < 15 seconds | < 20 seconds |

**Breakdown by Component**:
- **RAG Retrieval**: < 500ms (10% of total time)
- **LLM Generation**: < 2 seconds (40% of total time)
- **SQL Execution**: < 2 seconds (40% of total time)
- **Result Formatting**: < 500ms (10% of total time)

**Measurement Method**:
- Instrument each pipeline stage with timing metrics
- Log latency to Prometheus/time-series database
- Calculate percentiles hourly
- Alert when 95th percentile exceeds targets

**Validation**:
- Load testing with 100 diverse queries
- Measure under concurrent load (10 users)
- Test with production-sized database

---

### **NFR-1.2: LLM Inference Speed**

**Importance**: LLM processing is the most resource-intensive component. Slow inference creates bottlenecks and poor user experience.

#### **Metrics and Targets**

- **Tokens per second**: ≥ 30 tokens/second
- **Time to first token**: < 200ms
- **Maximum prompt length**: 2000 tokens (to maintain speed)
- **Response token limit**: 512 tokens

**Hardware Baseline**: 
- CPU: Intel Xeon or AMD EPYC (8+ cores)
- RAM: 16GB minimum for SQLCoder-7B
- No GPU required (CPU inference acceptable)

**Optimization Strategies**:
- Use quantized models (GGUF format, Q4 quantization)
- Implement prompt caching for repeated schema context
- Batch similar queries when possible
- Limit context window to essential information

**Measurement Method**:
- Monitor Ollama metrics endpoint
- Track tokens/second per request
- Profile memory usage during inference

---

### **NFR-1.3: Database Query Execution**

**Importance**: Database performance affects overall system responsiveness and prevents resource exhaustion on the SQL Server.

#### **Metrics and Targets**

- **Query timeout**: Hard limit at 30 seconds
- **Connection pool size**: 10-20 connections
- **Connection acquisition time**: < 100ms
- **Result set fetch time**: < 1 second for 1000 rows

**Database Performance Standards**:
- No table scans on large tables (>100K rows) without TOP clause
- JOINs use indexes when available
- Generated queries include appropriate WHERE filters
- LIMIT/TOP applied to prevent excessive result sets

**Resource Constraints**:
- Maximum 10 concurrent queries per database
- Read-only user with minimal permissions
- Query governor timeout enforced server-side
- Connection lifetime limited to 30 minutes

**Measurement Method**:
- Log SQL execution time from pyodbc
- Monitor database server metrics (CPU, I/O)
- Track slow query log
- Alert on queries exceeding 10 seconds

---

### **NFR-1.4: Vector Store Performance**

**Importance**: RAG retrieval must be fast to not bottleneck the overall pipeline. Slow similarity search degrades user experience.

#### **Metrics and Targets**

- **Similarity search**: < 500ms for top-5 results
- **Document count**: Support 10,000+ schema elements
- **Embedding generation**: < 100ms per query
- **Index size**: < 2GB for complete schema

**ChromaDB Configuration**:
- HNSW index for fast similarity search
- In-memory mode for maximum speed (with persistence)
- Batch embedding generation during schema ingestion
- Metadata filtering to narrow search space

**Measurement Method**:
- Time each ChromaDB query
- Monitor memory usage of vector store
- Track index build time during schema refresh
- Load test with 10 concurrent retrievals

---

### **NFR-1.5: UI Responsiveness**

**Importance**: The user interface must feel snappy and responsive to maintain user engagement and trust in the system.

#### **Metrics and Targets**

- **Initial page load**: < 2 seconds
- **Time to interactive**: < 3 seconds
- **Input lag**: < 50ms for typing
- **Result rendering**: < 500ms for 100 rows
- **History sidebar load**: < 200ms

**Client-Side Performance**:
- JavaScript bundle size: < 500KB (gzipped)
- CSS bundle size: < 100KB (gzipped)
- Lazy loading for non-critical components
- Virtualized tables for large result sets

**Measurement Method**:
- Lighthouse performance score ≥ 90
- WebPageTest timing metrics
- Real User Monitoring (RUM) if deployed
- Browser DevTools performance profiling

---

### **NFR-1.6: Throughput and Concurrency**

**Importance**: System must support multiple simultaneous users without degradation, especially during peak usage hours.

#### **Metrics and Targets**

| **Metric** | **Target** | **Constraint** |
|------------|------------|----------------|
| Concurrent users | 10-20 | Without performance degradation |
| Queries per minute | 60 | Sustained load |
| Peak queries per minute | 120 | Burst capacity (5 minutes) |
| Failed requests | < 1% | During normal operation |

**Concurrency Handling**:
- Request queuing for LLM inference (max queue: 10)
- Connection pooling for database (10-20 connections)
- Async processing for non-blocking operations
- Rate limiting: 10 queries per user per minute

**Measurement Method**:
- Load testing with JMeter or Locust
- Simulate 20 concurrent users
- Monitor queue depth and wait times
- Measure degradation curves under load

---

## **NFR-2: Security and Privacy Requirements**

**Category**: Security | **Priority**: CRITICAL | **Impact**: Very High

### **Description**
Healthcare data requires stringent security measures. The system must protect against unauthorized access, data breaches, and ensure compliance with HIPAA and other regulations.

---

### **NFR-2.1: Data Privacy and Confidentiality**

**Importance**: HIPAA compliance is mandatory for healthcare applications. Violations result in severe penalties ($100-$50,000 per violation) and loss of trust.

#### **Requirements**

**Local Processing Mandate**:
- **All data processing occurs on-premises**: Zero data transmission to external APIs
- **No cloud LLM services**: Ollama runs locally only
- **No telemetry or analytics**: Disable all external reporting
- **Air-gapped operation capable**: System functions without internet access

**PHI Protection Standards**:
- **No PHI in logs**: Mask patient identifiers, MRNs, names, SSNs
- **No PHI in error messages**: Generic errors only, details in secure logs
- **No PHI in UI examples**: Use synthetic data for demonstrations
- **No PHI in vector store**: Schema only, no actual patient data indexed

**Data-at-Rest Encryption**:
- **Vector store encryption**: ChromaDB data files encrypted with AES-256
- **Log file encryption**: Sensitive logs encrypted before storage
- **Configuration encryption**: Database passwords encrypted (not plaintext)
- **Backup encryption**: All backups encrypted end-to-end

**Data-in-Transit Encryption**:
- **TLS 1.3 for web interface**: HTTPS only, no HTTP fallback
- **Encrypted database connections**: TLS/SSL to SQL Server
- **Certificate validation**: No self-signed certs in production

**Measurement Method**:
- Security audit quarterly
- Penetration testing annually
- HIPAA compliance checklist verification
- Privacy Impact Assessment (PIA) before deployment

---

### **NFR-2.2: Authentication and Authorization**

**Importance**: Ensure only authorized users access the system and appropriate data. Prevents unauthorized data exposure.

#### **Requirements**

**Authentication Standards**:
- **Single Sign-On (SSO)**: Integration with organizational identity provider (SAML/OAuth2)
- **Multi-Factor Authentication (MFA)**: Required for all users
- **Session timeout**: 4 hours of inactivity, 8 hours maximum
- **Password requirements**: If local auth, 12+ characters, complexity rules

**Authorization Model**:
- **Role-Based Access Control (RBAC)**:
  - Admin: Full access, schema management, user management
  - Analyst: Query all databases, export data
  - Viewer: Query only, no export
  - Executive: Pre-defined queries, dashboards only

- **Database-level permissions**: User can only query databases they have SQL Server permissions for
- **Row-level security**: Respect database-level RLS policies
- **Column-level filtering**: Sensitive columns masked based on role

**Failed Login Protection**:
- Account lockout after 5 failed attempts
- 15-minute lockout duration
- Log all failed login attempts
- Alert security team on brute force patterns

**Measurement Method**:
- Quarterly access review
- Annual penetration testing of auth mechanisms
- Monitor failed login rates
- Audit trail of all access grants/revocations

---

### **NFR-2.3: SQL Injection Prevention**

**Importance**: SQL injection is the #1 web application vulnerability. Must prevent all forms of injection attacks to protect database integrity.

#### **Requirements**

**Input Validation**:
- **Whitelist validation**: Accept only alphanumeric, spaces, common punctuation
- **Length limits**: Maximum 500 characters for user input
- **Pattern blocking**: Reject known injection patterns (UNION, xp_, exec)
- **Encoding**: Properly escape all special characters

**Query Safety**:
- **Parameterized queries**: Never concatenate user input into SQL
- **Static analysis**: Scan generated SQL for injection patterns
- **Prepared statements**: Use database-level prepared statements
- **Read-only user**: Database account has SELECT permission only

**Validation Layers**:
1. Client-side: Basic input validation (UX improvement)
2. Application-side: Comprehensive validation before LLM
3. Post-LLM: Validate generated SQL before execution
4. Database-side: Enforce permissions at database level

**Testing Requirements**:
- Run OWASP ZAP automated scans monthly
- Manual penetration testing annually
- Include SQL injection test cases in CI/CD
- Test with fuzzing tools (SQLMap)

**Metrics**:
- Zero SQL injection vulnerabilities found in security scans
- 100% blocking rate on known injection patterns
- All injection attempts logged and alerted

---

### **NFR-2.4: Audit Logging and Compliance**

**Importance**: HIPAA requires comprehensive audit trails. Logs are essential for forensics, compliance audits, and detecting security incidents.

#### **Requirements**

**Audit Log Contents** (per HIPAA §164.312(b)):
- **User identification**: Username, role, session ID
- **Timestamp**: ISO 8601 format with timezone
- **Action performed**: Query submitted, data exported, schema accessed
- **Data accessed**: Tables queried, row counts (not actual data)
- **Outcome**: Success/failure, error codes
- **Source**: IP address, user agent, device ID

**Protected Health Information (PHI) Access Logs**:
- Log every query that accesses patient data tables
- Record specific patients accessed (by surrogate ID, not PHI)
- Track exports and downloads of patient-related data
- Flag unusual access patterns (volume, time, users)

**Log Retention**:
- **HIPAA minimum**: 6 years
- **Recommended**: 7 years for legal protection
- **Hot storage**: 90 days for quick access
- **Archive storage**: 7 years on cold storage

**Log Security**:
- **Immutable logs**: Write-once, prevent tampering
- **Encrypted storage**: Logs encrypted at rest
- **Access controls**: Only security admins can read logs
- **Integrity checking**: Cryptographic hashes to detect modification

**Compliance Mapping**:
- HIPAA §164.308(a)(1)(ii)(D) - Information System Activity Review
- HIPAA §164.312(b) - Audit Controls
- SOC 2 Type II - CC7.2 Monitoring Activities
- GDPR Article 30 - Records of Processing Activities (if applicable)

**Measurement Method**:
- Annual HIPAA compliance audit
- Quarterly log review by security team
- Automated log integrity checks daily
- Test log retrieval during incident response drills

---

### **NFR-2.5: Secure Configuration**

**Importance**: Misconfigurations are a leading cause of breaches. Secure defaults and hardening protect against common attacks.

#### **Requirements**

**Application Hardening**:
- **Debug mode disabled**: No debug endpoints or verbose errors in production
- **Error handling**: Generic error messages to users, details only in logs
- **Security headers**: CSP, X-Frame-Options, HSTS, X-Content-Type-Options
- **CORS restrictions**: Only allow configured origins
- **Remove default credentials**: No default passwords or API keys

**Database Security**:
- **Least privilege**: Application user has minimum necessary permissions
- **Strong passwords**: 20+ character complex passwords for DB accounts
- **Network isolation**: Database on private VLAN, not internet-accessible
- **Disable unused features**: xp_cmdshell, OLE Automation disabled
- **Regular patching**: Apply SQL Server security updates quarterly

**Dependency Security**:
- **Vulnerability scanning**: Scan dependencies with Snyk/Dependabot weekly
- **No known high/critical CVEs**: Update vulnerable packages within 7 days
- **License compliance**: Ensure all dependencies properly licensed
- **Minimal dependencies**: Reduce attack surface by limiting packages

**Secrets Management**:
- **No hardcoded secrets**: No passwords in source code
- **Environment variables**: Store secrets in .env (never committed)
- **Secrets rotation**: Rotate database passwords quarterly
- **Encrypted secrets**: Use HashiCorp Vault or similar for production

**Measurement Method**:
- Weekly vulnerability scans with automated tools
- Quarterly security configuration review
- Annual third-party security assessment
- Track mean time to patch critical vulnerabilities (target: <7 days)

---

## **NFR-3: Reliability and Availability Requirements**

**Category**: Reliability | **Priority**: HIGH | **Impact**: High

### **Description**
The system must be dependable and available during business hours. Downtime affects user productivity and trust in the system.

---

### **NFR-3.1: System Availability**

**Importance**: Users rely on the system for time-sensitive decisions. Unavailability during business hours is unacceptable.

#### **Metrics and Targets**

| **Metric** | **Target** | **Measurement Period** |
|------------|------------|------------------------|
| Uptime (business hours) | 99.5% | Monthly |
| Uptime (24/7) | 99.0% | Monthly |
| Planned downtime | < 4 hours/month | During maintenance windows |
| Unplanned downtime | < 30 minutes/month | Excluding force majeure |

**Business Hours Definition**: 
- Monday-Friday, 7 AM - 7 PM local time
- Excludes holidays per organizational calendar

**Availability Calculation**:
```
Availability % = (Total Time - Downtime) / Total Time × 100

99.5% uptime = ~3.6 hours downtime per month
99.0% uptime = ~7.3 hours downtime per month
```

**Measurement Method**:
- Health check endpoint every 60 seconds
- Uptime monitoring with Prometheus/Grafana
- Alert on 3 consecutive failed health checks
- Monthly availability report to stakeholders

---

### **NFR-3.2: Fault Tolerance**

**Importance**: Individual component failures should not cause total system failure. Graceful degradation maintains partial functionality.

#### **Requirements**

**Component Failure Handling**:

**LLM Service Failure**:
- **Retry logic**: 3 automatic retries with exponential backoff
- **Timeout**: 45-second timeout per attempt
- **Fallback**: Show cached similar queries or manual SQL option
- **User notification**: "AI service temporarily unavailable"

**Database Connection Failure**:
- **Connection pooling**: Automatic reconnection on dropped connections
- **Health checks**: Verify connection before query execution
- **Retry strategy**: Retry once after 2-second delay
- **Circuit breaker**: Disable queries after 5 consecutive failures (5 minutes)

**Vector Store Failure**:
- **Degraded mode**: Generate SQL without RAG context (lower accuracy)
- **Cache**: Use cached schema from last successful retrieval
- **Automatic recovery**: Reconnect when service restored
- **User notification**: "Operating with limited context"

**Disk Space Exhaustion**:
- **Monitoring**: Alert at 80% disk usage
- **Auto-cleanup**: Rotate logs automatically
- **Graceful degradation**: Disable logging if critical space threshold reached
- **User notification**: "System operating in limited mode"

**Measurement Method**:
- Chaos engineering tests quarterly
- Inject failures in test environment
- Measure recovery time for each failure type
- Track Mean Time To Recovery (MTTR): Target < 5 minutes

---

### **NFR-3.3: Data Integrity**

**Importance**: Results must be accurate and consistent. Data corruption or incorrect results undermine user trust and lead to bad decisions.

#### **Requirements**

**Query Result Accuracy**:
- **SQL correctness**: Generated SQL must be logically correct
- **No data corruption**: Read-only operations cannot corrupt database
- **Consistent results**: Same query returns same results (given unchanged data)
- **Transaction isolation**: Use READ COMMITTED or higher

**Schema Synchronization**:
- **Daily refresh**: Schema synchronized daily with production database
- **Change detection**: Alert on schema changes affecting active queries
- **Version control**: Track schema versions with timestamps
- **Validation**: Verify schema integrity after each refresh

**Log Integrity**:
- **Immutable logs**: Audit logs cannot be altered or deleted
- **Checksums**: Cryptographic hashes verify log file integrity
- **Backup logs**: Daily backup of logs to separate storage
- **Tamper detection**: Alert on any log modification attempts

**Measurement Method**:
- Weekly automated schema validation
- Monthly audit log integrity checks
- Compare query results against known ground truth dataset
- Zero tolerance for data integrity violations

---

### **NFR-3.4: Error Recovery**

**Importance**: System must recover gracefully from errors without manual intervention, maintaining user productivity.

#### **Requirements**

**Automatic Error Recovery**:

**Transient Errors** (network glitches, temporary database unavailability):
- Automatic retry up to 3 attempts
- Exponential backoff: 1s, 2s, 4s delays
- Log retry attempts
- Succeed silently if retry succeeds

**SQL Errors** (syntax errors, invalid table names):
- Parse error message from database
- Reformulate prompt with error context
- Retry SQL generation once
- If still fails, show error with suggestions

**Application Crashes**:
- Process supervisor (systemd, PM2) restarts service automatically
- Restart within 30 seconds
- Preserve user sessions in persistent storage
- Log crash dump for debugging

**Memory Leaks**:
- Monitor memory usage continuously
- Automatic restart if memory exceeds 90% of limit
- Scheduled restarts weekly during maintenance window
- Clear symptom detection before automatic action

**Recovery Metrics**:
- **MTTR (Mean Time To Recovery)**: < 5 minutes
- **MTBF (Mean Time Between Failures)**: > 720 hours (30 days)
- **Recovery success rate**: > 95% automatic recovery without human intervention

**Measurement Method**:
- Track error rates and recovery times
- Monthly reliability report
- Post-mortem for all failures requiring manual intervention
- Improve runbooks based on incident learnings

---

## **NFR-4: Scalability Requirements**

**Category**: Scalability | **Priority**: MEDIUM | **Impact**: Medium

### **Description**
The system must scale to accommodate growth in users, database size, and query complexity without requiring complete redesign.

---

### **NFR-4.1: User Scalability**

**Importance**: User base will grow over time. Architecture must support expansion without performance degradation.

#### **Metrics and Targets**

| **Growth Stage** | **Concurrent Users** | **Daily Active Users** | **Response Time** |
|------------------|----------------------|------------------------|-------------------|
| Initial (MVP) | 10 | 30 | < 5s (95th) |
| Phase 1 (6 months) | 25 | 75 | < 6s (95th) |
| Phase 2 (1 year) | 50 | 150 | < 7s (95th) |
| Phase 3 (2 years) | 100 | 300 | < 8s (95th) |

**Scaling Strategies**:

**Horizontal Scaling (Preferred)**:
- Deploy multiple Ollama instances behind load balancer
- Round-robin request distribution
- Session-sticky routing for conversation context
- Independent scaling of LLM, API, and DB layers

**Vertical Scaling (Short-term)**:
- Increase CPU cores for LLM inference
- Add RAM for larger models or more connections
- Faster SSDs for vector store performance

**Resource Requirements per 25 Users**:
- **CPU**: +4 cores
- **RAM**: +8 GB
- **Storage**: +5 GB for logs and vector store growth
- **Network**: +10 Mbps bandwidth

**Measurement Method**:
- Monthly user growth tracking
- Performance testing at each growth milestone
- Capacity planning sessions quarterly
- Alert when resource usage reaches 70% of capacity

---

### **NFR-4.2: Data Volume Scalability**

**Importance**: Database size and complexity grow over time. System must handle larger schemas and query volumes.

#### **Metrics and Targets**

| **Metric** | **Current** | **1 Year** | **2 Years** | **Maximum** |
|------------|-------------|------------|-------------|-------------|
| Tables | 500 | 750 | 1,000 | 2,000 |
| Columns | 10,000 | 15,000 | 20,000 | 50,000 |
| Schema docs in vector store | 5,000 | 10,000 | 15,000 | 30,000 |
| Historical queries stored | 10,000 | 50,000 | 100,000 | 500,000 |
| Daily query volume | 500 | 1,500 | 3,000 | 10,000 |

**Scaling Strategies**:

**Vector Store Optimization**:
- Partition schema by database or domain
- Implement hierarchical retrieval (database → table → column)
- Archive old query history to cold storage
- Periodic index optimization and compaction

**Database Query Optimization**:
- Cache frequently accessed schema metadata
- Index query history for fast retrieval
- Implement query result caching (5-minute TTL)
- Use materialized views for complex aggregations

**Schema Management**:
- Incremental schema updates (not full refresh each time)
- Lazy loading of detailed schema information
- Priority-based schema indexing (frequently used tables first)

**Measurement Method**:
- Track vector store size and query performance monthly
- Benchmark retrieval time as document count grows
- Test with synthetic large schemas (10,000+ tables)
- Monitor query performance degradation curves

---

### **NFR-4.3: Query Complexity Scalability**

**Importance**: As users become more sophisticated, they'll request more complex queries. System must handle increasing complexity.

#### **Requirements**

**Complexity Tiers**:

**Tier 1 - Simple** (80% of queries, < 3s target):
- Single table SELECT
- Basic WHERE filters
- Simple aggregations (COUNT, SUM)

**Tier 2 - Moderate** (15% of queries, < 8s target):
- 2-3 table JOINs
- Multiple WHERE conditions
- GROUP BY with HAVING

**Tier 3 - Complex** (4% of queries, < 15s target):
- 4-5 table JOINs
- Subqueries (1-2 levels)
- Window functions
- CTEs

**Tier 4 - Advanced** (1% of queries, < 30s target):
- 6+ table JOINs
- Nested subqueries (3+ levels)
- Complex analytical functions
- Recursive CTEs

**Complexity Handling**:
- Automatic complexity detection
- User warning for Tier 3+ queries
- Query optimization suggestions
- Option to simplify or break into multiple queries
- Caching results for identical complex queries

**Measurement Method**:
- Track query complexity distribution
- Monitor success rate by complexity tier
- Identify common complex patterns for optimization
- User satisfaction correlation with complexity

---

## **NFR-5: Maintainability Requirements**

**Category**: Maintainability | **Priority**: HIGH | **Impact**: Medium

### **Description**
The system must be easy to understand, modify, and extend by current and future developers. Good maintainability reduces long-term costs and enables rapid feature development.

---

### **NFR-5.1: Code Quality**

**Importance**: High-quality code reduces bugs, accelerates feature development, and lowers onboarding time for new developers.

#### **Metrics and Targets**

| **Metric** | **Target** | **Tool** |
|------------|------------|----------|
| Test coverage | ≥ 80% | pytest-cov |
| Linting compliance | 100% (no warnings) | ruff, pylint |
| Type coverage | ≥ 90% | mypy |
| Code complexity | < 10 cyclomatic complexity per function | radon |
| Documentation coverage | 100% of public APIs | sphinx |
| Code duplication | < 5% | pylint |

**Code Standards**:
- **PEP 8 compliance**: Enforce with automated linting
- **Type hints**: Required for all function signatures
- **Docstrings**: Required for all public functions/classes (Google style)
- **Naming conventions**: Descriptive variable names, no single letters except loops
- **Function length**: Maximum 50 lines per function
- **Class size**: Maximum 300 lines per class

**Automated Enforcement**:
- Pre-commit hooks run linters and formatters
- CI/CD pipeline fails on linting errors
- Code review checklist includes quality criteria
- Weekly automated quality reports

**Measurement Method**:
- SonarQube or Code Climate analysis weekly
- Track technical debt score
- Measure time to fix bugs (target: < 2 days for P2 bugs)
- Developer satisfaction surveys on code quality

---

### **NFR-5.2: Documentation**

**Importance**: Comprehensive documentation accelerates onboarding, reduces support burden, and enables independent problem-solving.

#### **Requirements**

**Developer Documentation**:
- **Architecture diagrams**: System components, data flows, deployment
- **API reference**: Auto-generated from docstrings
- **Setup guide**: Step-by-step local development setup (< 30 minutes)
- **Contributing guide**: How to submit changes, coding standards
- **Decision records**: ADRs for major architectural decisions

**User Documentation**:
- **User manual**: End-user guide with screenshots
- **Query pattern library**: Examples of supported query types
- **Troubleshooting guide**: Common errors and solutions
- **FAQ**: Top 20 user questions answered
- **Video tutorials**: 5-10 minute walkthrough videos

**Operational Documentation**:
- **Deployment guide**: Production deployment steps
- **Monitoring guide**: How to read dashboards and alerts
- **Incident response runbook**: Step-by-step for common issues
- **Backup and recovery**: Disaster recovery procedures
- **Configuration reference**: All environment variables documented

**Documentation Standards**:
- Markdown format for version control
- Kept in repository alongside code
- Updated with every feature release
- Reviewed during code review process
- Versioned to match software releases

**Measurement Method**:
- Documentation completeness checklist (100% target)
- Track time-to-productivity for new developers (target: < 1 week)
- User feedback on documentation helpfulness
- Monitor support ticket volume (decrease expected with better docs)

---

### **NFR-5.3: Logging and Observability**

**Importance**: Comprehensive logging enables fast debugging, performance optimization, and proactive issue detection.

#### **Requirements**

**Logging Standards**:
- **Structured logging**: JSON format with consistent schema
- **Log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL used appropriately
- **Context inclusion**: Request ID, user ID, session ID in all logs
- **Sensitive data masking**: PHI never logged
- **Correlation IDs**: Track requests across components

**Log Content by Level**:

**DEBUG** (development only):
- Function entry/exit
- Variable values
- Detailed execution flow

**INFO** (production):
- Request received/completed
- Query execution started/finished
- Schema refresh completed
- User login/logout

**WARNING**:
- Slow query (>10s)
- Retry attempts
- Degraded mode operation
- Approaching resource limits

**ERROR**:
- Query execution failed
- LLM service unavailable
- Database connection lost
- Validation failures

**CRITICAL**:
- Service crash
- Security breach detected
- Data integrity violation
- System unrecoverable without intervention

**Observability Stack**:
- **Metrics**: Prometheus for time-series metrics
- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana) or Loki
- **Traces**: OpenTelemetry for distributed tracing (optional)
- **Dashboards**: Grafana for visualization
- **Alerting**: Alertmanager for incident notification

**Key Metrics Collected**:
- Query latency (p50, p95, p99)
- Error rates by component
- LLM tokens per second
- Database connection pool utilization
- Memory and CPU usage
- Active user sessions

**Measurement Method**:
- 100% of errors logged with stack traces
- Mean Time To Detection (MTTD) < 5 minutes for critical issues
- Mean Time To Investigation (MTTI) < 15 minutes (with good logs)
- Quarterly review of logging coverage

---

### **NFR-5.4: Configuration Management**

**Importance**: Externalized configuration enables easy environment management and prevents hard-coding of environment-specific values.

#### **Requirements**

**Configuration Externalization**:
- **Environment variables**: All environment-specific configs
- **Configuration files**: YAML for complex structured configs
- **Secrets management**: External secrets store (HashiCorp Vault) or encrypted
- **No secrets in code**: Secrets never committed to git

**Configuration Categories**:

**Database Configuration** (`config/database.yaml`):
```yaml
sql_server:
  host: ${DB_HOST}
  port: ${DB_PORT}
  database: ${DB_NAME}
  connection_pool:
    min_size: 5
    max_size: 20
    timeout: 30
```

**LLM Configuration** (`config/ollama.yaml`):
```yaml
ollama:
  base_url: http://localhost:11434
  model: sqlcoder:7b-q4
  temperature: 0.1
  max_tokens: 512
  timeout: 45
```

**RAG Configuration** (`config/rag.yaml`):
```yaml
vector_store:
  provider: chromadb
  collection_name: sql_schema
  embedding_model: all-MiniLM-L6-v2
  top_k: 5
  similarity_threshold: 0.7
```

**Environment-Specific Configs**:
- Development: Verbose logging, debug mode, test database
- Staging: Production-like, synthetic data, monitoring enabled
- Production: Error-only logs, security hardened, real data

**Measurement Method**:
- Zero secrets in git history (scan with truffleHog)
- Configuration changes via pull requests only
- Audit trail of all configuration modifications
- Successful deployment to new environment without code changes

---

## **NFR-6: Usability Requirements**

**Category**: Usability | **Priority**: HIGH | **Impact**: High

### **Description**
The system must be intuitive and easy to use for non-technical users. Poor usability leads to low adoption and user frustration.

---

### **NFR-6.1: Learnability**

**Importance**: Users should become productive quickly without extensive training. Steep learning curves deter adoption.

#### **Metrics and Targets**

- **Time to first successful query**: < 5 minutes for new users
- **Time to proficiency**: < 2 hours total usage
- **Unassisted task completion**: 80% of tasks completed without help after training
- **Training time required**: < 30 minutes initial orientation

**Learnability Features**:

**Progressive Disclosure**:
- Simple interface by default
- Advanced features hidden until needed
- Contextual help appears when relevant
- Gradual introduction of complexity

**In-App Guidance**:
- Interactive tutorial on first login
- Tooltips explain each UI element
- Example queries readily accessible
- Suggested next steps after each query

**Error Prevention**:
- Autocomplete prevents typos
- Validation before submission
- Clear warnings for risky actions
- Undo functionality where applicable

**Measurement Method**:
- User testing with 5-10 new users
- Task completion rates and times
- Pre/post-training competency assessments
- Net Promoter Score (NPS) survey

---

### **NFR-6.2: Efficiency of Use**

**Importance**: Experienced users should be able to work quickly without unnecessary steps or cognitive load.

#### **Metrics and Targets**

- **Keystrokes per query**: < 50 for common queries (via templates/history)
- **Clicks per query**: ≤ 3 clicks (input → submit → result)
- **Time per query**: < 30 seconds for repeat queries
- **Keyboard shortcuts**: 10+ shortcuts for power users

**Efficiency Features**:

**Keyboard Shortcuts**:
- `Ctrl+Enter`: Submit query
- `Ctrl+K`: Focus search
- `Ctrl+H`: Toggle history
- `Ctrl+E`: Export results
- `Ctrl+C`: Copy SQL
- `Ctrl+/`: Show shortcuts

**Quick Actions**:
- Click history item to re-run
- Modify last query from history
- Save frequent queries as templates
- One-click export to CSV/Excel

**Smart Defaults**:
- Remember last database selected
- Auto-fill date ranges (defaults to "last month")
- Preserve sorting preferences
- Cache user preferences

**Measurement Method**:
- Time-on-task studies with experienced users
- Track keyboard shortcut usage rates
- Efficiency metrics vs baseline (manual SQL writing)
- User satisfaction surveys on productivity

---

### **NFR-6.3: Accessibility**

**Importance**: System must be usable by people with disabilities, meeting legal requirements (ADA, Section 508) and ethical obligations.

#### **Standards and Targets**

- **WCAG 2.1 Level AA compliance**: Minimum legal requirement
- **Screen reader compatibility**: JAWS, NVDA, VoiceOver
- **Keyboard navigation**: 100% functionality without mouse
- **Color contrast**: Minimum 4.5:1 for normal text, 3:1 for large text

**Accessibility Requirements**:

**Visual Accessibility**:
- High contrast mode available
- Text resizable up to 200% without loss of functionality
- No information conveyed by color alone
- Focus indicators clearly visible
- Minimum 16px font size for body text

**Motor Accessibility**:
- All functionality available via keyboard
- Target size minimum 44x44 pixels for touch
- No time-limited actions (or generous extensions)
- Skip navigation links for screen readers
- Adjustable animation (or disable animations)

**Auditory Accessibility**:
- No audio-only content (not applicable)
- Captions for any video tutorials

**Cognitive Accessibility**:
- Consistent navigation and layout
- Clear, simple language (8th grade reading level)
- Error messages with clear recovery steps
- Undo functionality for destructive actions
- Reduce cognitive load with progressive disclosure

**Assistive Technology Support**:
- ARIA labels on all interactive elements
- Semantic HTML structure
- Table headers properly associated
- Form labels explicitly connected to inputs
- Status messages announced to screen readers

**Measurement Method**:
- Automated WCAG testing (axe, WAVE) in CI/CD
- Manual screen reader testing monthly
- Accessibility audit by certified specialist annually
- User testing with people with disabilities
- Zero critical accessibility issues in production

---

### **NFR-6.4: User Satisfaction**

**Importance**: User satisfaction directly correlates with adoption and continued usage. Dissatisfied users abandon the system.

#### **Metrics and Targets**

| **Metric** | **Target** | **Measurement** |
|------------|------------|-----------------|
| System Usability Scale (SUS) | ≥ 75 (Good) | Quarterly survey |
| Net Promoter Score (NPS) | ≥ 30 (Good) | Quarterly survey |
| User satisfaction rating | ≥ 4.0/5.0 | Post-interaction surveys |
| Task success rate | ≥ 85% | User testing observations |
| User retention rate | ≥ 75% at 3 months | Usage analytics |

**Satisfaction Drivers**:
- Speed: Fast responses reduce frustration
- Accuracy: Correct SQL builds trust
- Reliability: Consistent uptime expected
- Helpfulness: Good error messages and suggestions
- Aesthetics: Pleasant, modern interface

**Feedback Collection**:
- In-app feedback button
- Quarterly user surveys
- Quarterly user interviews (5-10 users)
- Usage analytics and funnel analysis
- Support ticket sentiment analysis

**Measurement Method**:
- Quarterly SUS and NPS surveys (minimum 30 responses)
- Track scores over time to measure improvement
- Segment by user persona to identify pain points
- Action plan for any score below target
- Close the loop: Communicate improvements to users

---

## **NFR-7: Compatibility Requirements**

**Category**: Compatibility | **Priority**: MEDIUM | **Impact**: Medium

### **Description**
The system must work across various platforms, browsers, and database versions to maximize accessibility and deployment flexibility.

---

### **NFR-7.1: Browser Compatibility**

**Importance**: Users work on diverse devices. System must function consistently across modern browsers.

#### **Supported Browsers** (Last 2 major versions)

| **Browser** | **Minimum Version** | **Market Share** |
|-------------|---------------------|------------------|
| Google Chrome | 120+ | ~65% |
| Mozilla Firefox | 120+ | ~10% |
| Microsoft Edge | 120+ | ~15% |
| Safari (macOS/iOS) | 16+ | ~10% |

**Not Supported**:
- Internet Explorer (EOL)
- Browsers older than 2 years

**Responsive Design**:
- Desktop: ≥ 1200px width (optimal experience)
- Tablet: 768-1199px (functional, adapted layout)
- Mobile: ≥ 375px (limited use cases, query submission)

**Testing Requirements**:
- Cross-browser testing in CI/CD (BrowserStack or Selenium Grid)
- Manual testing on primary browsers each release
- Responsive testing at 3 breakpoints
- Touch gesture support on mobile devices

**Measurement Method**:
- Browser usage analytics
- Bug reports segmented by browser
- Visual regression testing screenshots
- User-reported compatibility issues < 2% of tickets

---

### **NFR-7.2: Operating System Compatibility**

**Importance**: Deployment flexibility requires support for multiple server operating systems.

#### **Supported Server OS**

| **OS** | **Minimum Version** | **Status** |
|--------|---------------------|------------|
| Ubuntu Linux | 20.04 LTS | Recommended |
| Red Hat Enterprise Linux | 8.x | Supported |
| Windows Server | 2019 | Supported |
| CentOS/Rocky Linux | 8.x | Supported |
| macOS | 12+ (Monterey) | Development only |

**Installation Requirements**:
- Python 3.9-3.11
- Ollama compatible OS
- SQL Server client libraries (pyodbc/FreeTDS)
- Minimum 16GB RAM, 8-core CPU

**Testing Requirements**:
- Automated tests run on Ubuntu (primary)
- Manual testing on Windows Server quarterly
- Docker image for OS abstraction
- CI/CD tests in Linux containers

---

### **NFR-7.3: Database Compatibility**

**Importance**: Organization may upgrade SQL Server versions. System should support multiple versions.

#### **Supported Database Versions**

| **Database** | **Minimum Version** | **Status** |
|--------------|---------------------|------------|
| SQL Server | 2016 | Minimum |
| SQL Server | 2017-2022 | Fully tested |
| Azure SQL Database | Current | Supported |
| SQL Server on Linux | 2017+ | Supported |

**T-SQL Compatibility**:
- Avoid version-specific features unless necessary
- Use compatibility_level appropriate for minimum version
- Detect server version and adapt queries
- Document minimum SQL Server version requirement

**Future Extensibility**:
- Abstraction layer for SQL generation
- Database-specific prompt templates
- Potential support for PostgreSQL, MySQL, Oracle

**Testing Requirements**:
- Automated tests against SQL Server 2016, 2019, 2022
- Test both on-premises and Azure SQL
- Compatibility matrix documented
- Version detection on connection

**Measurement Method**:
- Zero compatibility issues reported from supported versions
- Successful deployments on all supported databases
- Automated compatibility tests in CI/CD

---

## **NFR-8: Portability Requirements**

**Category**: Portability | **Priority**: MEDIUM | **Impact**: Medium

### **Description**
The system should be easy to deploy and move between environments with minimal configuration changes.

---

### **NFR-8.1: Deployment Flexibility**

**Importance**: Different organizations have different infrastructure. System must adapt to various deployment models.

#### **Supported Deployment Models**

**Bare Metal / VM**:
- Install directly on server
- systemd service for Linux
- Windows Service for Windows
- Manual startup for development

**Docker Container**:
- Official Docker images published
- Docker Compose for multi-container setup
- Environment-based configuration
- Volume mounts for persistence

**Kubernetes** (Future):
- Helm charts for deployment
- Horizontal pod autoscaling
- StatefulSet for vector store
- ConfigMaps and Secrets

**Requirements**:
- Single-command deployment for Docker
- Deployment guide for each model
- Environment variable configuration
- No hard-coded paths or assumptions

**Measurement Method**:
- Successful deployment on 3 different infrastructure types
- Deployment time < 30 minutes (excluding model download)
- Zero environment-specific code changes needed

---

### **NFR-8.2: Data Portability**

**Importance**: Users may need to migrate systems, back up data, or export for analysis.

#### **Requirements**

**Export Capabilities**:
- **Query history**: Export to JSON/CSV
- **Schema snapshots**: Export complete schema definition
- **User queries**: Bulk export for analysis
- **Configuration**: Export settings for migration

**Import Capabilities**:
- **Schema import**: Restore from exported schema
- **Example queries**: Import curated query libraries
- **Configuration**: Import settings to new installation

**Backup and Restore**:
- **Vector store**: Backup ChromaDB collections
- **Application data**: Backup query history, user preferences
- **Restoration time**: < 15 minutes for complete restore

**Measurement Method**:
- Quarterly backup and restore drill
- Successful data migration between environments
- Zero data loss during migration
- Complete audit trail preserved

---

## **Summary: Non-Functional Requirements**

### **NFR Priority Matrix**

| **Category** | **Priority** | **Key Metrics** | **Business Impact** |
|--------------|--------------|-----------------|---------------------|
| Performance | CRITICAL | < 5s response, 30 tok/s LLM | User productivity |
| Security | CRITICAL | HIPAA compliant, zero breaches | Legal compliance |
| Reliability | HIGH | 99.5% uptime, < 5m MTTR | User trust |
| Maintainability | HIGH | 80% test coverage, docs | Long-term cost |
| Usability | HIGH | SUS ≥ 75, < 5m learning | Adoption rate |
| Scalability | MEDIUM | 100 users, 2000 tables | Future growth |
| Compatibility | MEDIUM | Modern browsers, SQL 2016+ | Deployment reach |
| Portability | MEDIUM | Docker ready, data export | Operational flexibility |

### **Measurement and Monitoring Strategy**

**Automated Monitoring**:
- Prometheus metrics collection every 30 seconds
- Grafana dashboards for real-time visualization
- Automated alerts for threshold breaches
- Weekly automated reports

**Manual Assessment**:
- Monthly security review
- Quarterly user satisfaction surveys
- Quarterly load testing
- Annual third-party security audit

**Continuous Improvement**:
- NFR metrics reviewed in monthly team meetings
- Remediation plans for below-target metrics
- User feedback incorporated into roadmap
- Quarterly retrospectives on system quality

These non-functional requirements ensure the system is not only functional but also secure, reliable, performant, maintainable, and user-friendly—critical factors for long-term success and user adoption in a healthcare environment.