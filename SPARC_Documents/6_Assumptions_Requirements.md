# **Assumptions: Local LLM RAG SQL Query Application**

---

[Back to Main SPARC Documentation](SQL%20LLM%20RAG%20Project%20SPARC.md)

## **Overview**

Assumptions represent underlying beliefs, dependencies, and expectations that influence design decisions but are not explicitly guaranteed. This section documents all assumptions made during the specification process, their justifications, impacts, and associated risks. Proper assumption documentation ensures stakeholders understand project constraints and dependencies.

**Assumption Categories**:
- Technical Infrastructure
- User Behavior and Knowledge
- Data and Database
- Organizational Context
- Resource Availability
- Security and Compliance
- Integration and Dependencies
- Performance and Scale

---

## **1. Technical Infrastructure Assumptions**

### **A-1.1: Adequate Hardware Resources Available**

**Assumption**: Deployment servers have minimum 16GB RAM, 8-core CPU, and 100GB available disk space.

**Justification**:
- SQLCoder-7B requires ~8GB RAM for inference
- ChromaDB vector store needs 2-4GB RAM
- Application overhead requires 2-3GB RAM
- Schema data and query history need storage
- Concurrent user sessions require CPU resources

**Impact if Correct**:
✅ System runs smoothly with acceptable performance  
✅ Can support 10-20 concurrent users  
✅ LLM inference completes within 2-3 seconds  
✅ No resource-related crashes or slowdowns  

**Risk if Incorrect**:
❌ **High Impact** - System becomes unusable if resources insufficient  
❌ Slow query processing (>10 seconds)  
❌ Out-of-memory errors during peak usage  
❌ Inability to run Ollama and application simultaneously  
❌ Poor user experience leading to abandonment  

**Validation Method**:
```bash
# Pre-deployment hardware verification
scripts/deployment/verify_resources.sh

Required checks:
- RAM: free -h (minimum 16GB available)
- CPU: lscpu (minimum 8 cores)
- Disk: df -h (minimum 100GB free)
- GPU: nvidia-smi (optional but recommended)
```

**Mitigation Strategy**:
- **Plan A**: Scale down to smaller model (SQLCoder-3B uses 4GB RAM)
- **Plan B**: Implement request queuing to handle resource constraints
- **Plan C**: Deploy to cloud with auto-scaling capabilities
- **Plan D**: Optimize code for lower resource usage (quantization, caching)

**Assumption Owner**: Infrastructure Team  
**Verification Deadline**: Before deployment  
**Priority**: CRITICAL

---

### **A-1.2: Local Network Access to Database**

**Assumption**: Application server can reach SQL Server database on the local network without requiring internet connectivity.

**Justification**:
- Healthcare environments typically air-gapped for security
- Low latency database access required for good performance
- Compliance requirements often mandate local processing
- Assumption aligns with HIPAA security requirements

**Impact if Correct**:
✅ Fast database queries (<500ms network latency)  
✅ No external network dependencies  
✅ Enhanced security posture  
✅ Compliance with data sovereignty requirements  

**Risk if Incorrect**:
❌ **Medium Impact** - High latency affects user experience  
❌ VPN/network issues cause downtime  
❌ Additional infrastructure costs for connectivity  
❌ Potential compliance violations if data traverses internet  

**Validation Method**:
```python
# Network connectivity test
def test_database_connectivity():
    import socket
    import time
    
    host = os.getenv('DB_HOST')
    port = int(os.getenv('DB_PORT', 1433))
    
    start = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    latency = (time.time() - start) * 1000
    
    assert result == 0, f"Cannot reach database at {host}:{port}"
    assert latency < 100, f"High latency: {latency}ms"
    print(f"✓ Database reachable with {latency:.2f}ms latency")
```

**Mitigation Strategy**:
- Configure connection pooling for unstable networks
- Implement automatic retry with exponential backoff
- Cache frequently accessed schema data locally
- Deploy application closer to database (same data center)

**Assumption Owner**: Network Team  
**Verification Deadline**: During setup  
**Priority**: HIGH

---

### **A-1.3: Ollama Service Runs Reliably**

**Assumption**: Ollama service (or alternative local LLM runtime) can be installed and runs stably on the target operating system.

**Justification**:
- Ollama has broad OS support (Linux, macOS, Windows)
- Active development and community support
- Production deployments exist in similar environments
- Fallback options available (llama.cpp, vLLM)

**Impact if Correct**:
✅ Seamless LLM integration  
✅ Easy model management and updates  
✅ Good inference performance  
✅ Simplified deployment  

**Risk if Incorrect**:
❌ **Critical Impact** - Core functionality unavailable  
❌ Must rewrite LLM integration layer  
❌ Potential delays in project timeline  
❌ May need alternative runtime (llama.cpp, vLLM)  

**Validation Method**:
```bash
# Ollama installation and health check
scripts/setup/install_ollama.sh
ollama --version
ollama pull sqlcoder:7b-q4
ollama run sqlcoder:7b-q4 "SELECT 1" --timeout 30s
```

**Mitigation Strategy**:
- **Abstraction Layer**: Create LLM interface to allow runtime swapping
- **Alternative Runtimes**: Pre-test llama.cpp and vLLM as backups
- **Documentation**: Maintain setup guides for all supported runtimes
- **Containerization**: Use Docker to ensure consistent environment

**Assumption Owner**: DevOps Team  
**Verification Deadline**: During initial setup  
**Priority**: CRITICAL

---

### **A-1.4: No GPU Required for Acceptable Performance**

**Assumption**: CPU-only inference provides acceptable performance (<5 seconds per query) for production use.

**Justification**:
- Quantized models (Q4) run efficiently on modern CPUs
- Query generation is not real-time critical (users accept 3-5s delay)
- GPU availability varies across healthcare environments
- Cost and complexity reduction without GPU requirement

**Impact if Correct**:
✅ Broader deployment compatibility  
✅ Lower infrastructure costs  
✅ Simplified deployment process  
✅ No GPU driver/CUDA dependencies  

**Risk if Incorrect**:
❌ **Medium Impact** - Slow inference frustrates users  
❌ May need GPU to meet performance targets  
❌ Additional infrastructure costs ($2000-5000 per GPU)  
❌ Increased deployment complexity  

**Validation Method**:
```python
# Performance benchmark
def benchmark_cpu_inference():
    import time
    from ollama import Client
    
    client = Client()
    queries = [
        "How many patients admitted yesterday?",
        "Show me census by unit",
        "Calculate readmission rates"
    ]
    
    times = []
    for query in queries:
        start = time.time()
        response = client.generate(
            model='sqlcoder:7b-q4',
            prompt=f"Generate SQL: {query}"
        )
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"Query: {query[:30]}... - {elapsed:.2f}s")
    
    avg_time = sum(times) / len(times)
    assert avg_time < 5.0, f"Average inference time {avg_time:.2f}s exceeds 5s target"
    print(f"✓ Average inference time: {avg_time:.2f}s")
```

**Mitigation Strategy**:
- Optimize prompt length to reduce token count
- Use smaller model variant if performance inadequate (SQLCoder-3B)
- Implement caching for repeated queries
- Consider GPU deployment as upgrade path if needed
- Use quantization (Q4 vs Q8) for speed vs accuracy tradeoff

**Assumption Owner**: Performance Team  
**Verification Deadline**: During benchmarking phase  
**Priority**: HIGH

---

## **2. User Behavior and Knowledge Assumptions**

### **A-2.1: Users Have Limited SQL Knowledge**

**Assumption**: Primary users have little to no SQL expertise and need natural language interface.

**Justification**:
- Project goal explicitly states "democratizing data access"
- User personas (Sarah, Dr. Johnson) defined as non-technical
- Healthcare operational staff typically lack programming skills
- Market research shows 80%+ of potential users can't write SQL

**Impact if Correct**:
✅ Product fulfills core value proposition  
✅ UI design appropriately simplified  
✅ Help system and examples critical for success  
✅ Training requirements manageable  

**Risk if Incorrect**:
❌ **Low Impact** - Feature still valuable even for SQL-capable users  
❌ May need additional power user features  
❌ Advanced users might prefer direct SQL editor  
❌ Missing optimization for expert workflows  

**Validation Method**:
- User interviews: "How comfortable are you writing SQL queries?" (1-10 scale)
- Pre-deployment survey: SQL knowledge assessment
- Usage analytics: Track SQL query editor usage vs NL interface
- Support ticket analysis: Count SQL-related help requests

**Mitigation Strategy**:
- Provide SQL editor as advanced feature for power users
- Show generated SQL for educational purposes
- Allow query refinement via SQL editing
- Create tutorial progression (beginner → intermediate → advanced)

**Assumption Owner**: Product Team  
**Verification Deadline**: User research phase  
**Priority**: MEDIUM

---

### **A-2.2: Users Understand Healthcare Domain Terminology**

**Assumption**: Users know healthcare terms ("discharge", "census", "readmission") but not database column names.

**Justification**:
- Target audience works in healthcare industry
- Domain knowledge prerequisite for job function
- Gap is technical database structure, not business concepts
- Training focuses on system usage, not domain education

**Impact if Correct**:
✅ Can use healthcare terminology in prompts  
✅ No need for extensive domain glossary  
✅ Users understand query results context  
✅ Faster user onboarding  

**Risk if Incorrect**:
❌ **Medium Impact** - Users confused by terminology  
❌ Need extensive tooltips and help text  
❌ More support burden explaining concepts  
❌ Longer training requirements  

**Validation Method**:
- User testing: Present sample queries with healthcare terms
- Comprehension assessment: "What does this query ask?"
- Feedback surveys: Rate understanding of terminology (1-5 scale)
- Support ticket analysis: Track terminology-related questions

**Mitigation Strategy**:
- Provide in-app glossary of healthcare terms
- Tooltips explain abbreviations (DRG, LOS, ALOS, etc.)
- Include term definitions in example queries
- Link to external healthcare data dictionaries

**Assumption Owner**: Product Team  
**Verification Deadline**: User testing phase  
**Priority**: MEDIUM

---

### **A-2.3: Users Accept 3-5 Second Query Response Time**

**Assumption**: Users tolerate brief delays for natural language query processing, similar to web search.

**Justification**:
- Users familiar with web search (Google ~0.5-2s)
- AI tools like ChatGPT set expectation of 2-5s responses
- Healthcare reports traditionally take minutes/hours to generate
- Trade-off: convenience vs speed is acceptable

**Impact if Correct**:
✅ Performance targets are achievable  
✅ CPU-only deployment viable  
✅ No need for expensive optimization  
✅ User satisfaction maintained  

**Risk if Incorrect**:
❌ **High Impact** - User frustration and abandonment  
❌ Need significant performance optimization  
❌ May require GPU acceleration  
❌ Competitive disadvantage vs instant tools  

**Validation Method**:
```python
# User experience testing
def measure_user_tolerance():
    # A/B test different response times
    groups = {
        'A': 2.0,  # 2 second responses
        'B': 4.0,  # 4 second responses
        'C': 6.0,  # 6 second responses
    }
    
    # Track:
    # - Task completion rate
    # - User satisfaction rating
    # - Number of query retries
    # - Session abandonment rate
    
    # Acceptable thresholds:
    # - >85% completion rate
    # - >4.0/5.0 satisfaction
    # - <10% abandonment
```

**Mitigation Strategy**:
- Show progress indicators during processing
- Break down wait time: "Understanding... Generating SQL... Executing..."
- Implement query result caching for repeat queries
- Optimize hot paths (common query patterns)
- Set clear expectations: "This usually takes 3-5 seconds"

**Assumption Owner**: UX Team  
**Verification Deadline**: User acceptance testing  
**Priority**: HIGH

---

### **A-2.4: Users Prefer Conversational Follow-Up Over New Queries**

**Assumption**: Users want to refine queries through conversation ("show me the top 10", "break it down by unit") rather than rewriting from scratch.

**Justification**:
- Natural human communication pattern
- ChatGPT and similar tools trained users to expect conversation
- Reduces cognitive load vs reformulating entire query
- Faster iterative analysis workflow

**Impact if Correct**:
✅ Conversation memory features highly valued  
✅ Differentiation from traditional BI tools  
✅ Better user experience for exploratory analysis  
✅ Increased engagement and usage  

**Risk if Incorrect**:
❌ **Low Impact** - Feature still useful but less critical  
❌ Development effort could be redirected  
❌ Conversation context may confuse some users  
❌ Need clear "start new query" affordance  

**Validation Method**:
- Usage analytics: Track follow-up query frequency
- User interviews: "How do you prefer to refine results?"
- A/B testing: Conversation mode vs independent queries
- Session analysis: Average queries per conversation thread

**Mitigation Strategy**:
- Make conversation reset obvious and accessible
- Show conversation context in UI (breadcrumbs)
- Allow editing previous queries from history
- Provide both conversation and independent query modes

**Assumption Owner**: Product Team  
**Verification Deadline**: Beta testing phase  
**Priority**: MEDIUM

---

## **3. Data and Database Assumptions**

### **A-3.1: Database Schema is Relatively Stable**

**Assumption**: Database schema changes infrequently (monthly or less), not daily or weekly.

**Justification**:
- Enterprise databases typically have formal change management
- Healthcare data warehouses are relatively stable
- Schema changes require testing and approval processes
- Historical pattern analysis supports this assumption

**Impact if Correct**:
✅ Daily schema refresh adequate  
✅ Vector store doesn't need constant updates  
✅ Lower operational overhead  
✅ Cached schema data remains valid  

**Risk if Incorrect**:
❌ **Medium Impact** - Queries fail on changed tables  
❌ User frustration from outdated schema  
❌ Need more frequent refresh cycles  
❌ Increased system load from frequent indexing  

**Validation Method**:
```sql
-- Monitor schema changes
SELECT 
    OBJECT_NAME(object_id) as table_name,
    modify_date,
    DATEDIFF(day, modify_date, GETDATE()) as days_since_change
FROM sys.tables
WHERE modify_date > DATEADD(month, -3, GETDATE())
ORDER BY modify_date DESC;

-- Alert on frequent changes
-- Threshold: >5 schema changes per week indicates instability
```

**Mitigation Strategy**:
- Implement configurable refresh intervals (daily, weekly, on-demand)
- Detect schema changes and alert administrators
- Graceful degradation when schema mismatch detected
- Version schema snapshots for rollback capability
- Schema change notification webhook integration

**Assumption Owner**: Database Team  
**Verification Deadline**: First month of production  
**Priority**: MEDIUM

---

### **A-3.2: Database Contains Consistent, Quality Data**

**Assumption**: Data in the database is reasonably clean, consistent, and follows expected patterns (dates are dates, numbers are numbers, no excessive nulls).

**Justification**:
- Production databases typically have data quality processes
- Healthcare systems enforce data validation at entry
- Regulatory requirements mandate data quality
- Critical business decisions depend on data accuracy

**Impact if Correct**:
✅ SQL queries return meaningful results  
✅ No need for extensive data cleaning  
✅ Aggregations and calculations work correctly  
✅ User trust in results maintained  

**Risk if Incorrect**:
❌ **High Impact** - Incorrect results damage trust  
❌ Need data quality checks before queries  
❌ NULL handling logic becomes complex  
❌ May need data cleaning pipeline  

**Validation Method**:
```python
# Data quality assessment
def assess_data_quality(table_name):
    checks = {
        'null_percentage': """
            SELECT 
                column_name,
                COUNT(*) - COUNT(column_name) as null_count,
                CAST(COUNT(*) - COUNT(column_name) AS FLOAT) / COUNT(*) * 100 as null_pct
            FROM information_schema.columns
            WHERE table_name = ?
        """,
        'date_ranges': """
            SELECT 
                MIN(admit_date) as earliest,
                MAX(admit_date) as latest,
                COUNT(*) as total
            FROM pt_accounting_reporting_alt
            WHERE admit_date > '1900-01-01' AND admit_date < GETDATE()
        """,
        'referential_integrity': """
            -- Check for orphaned foreign keys
            SELECT COUNT(*) as orphaned_records
            FROM table_a a
            LEFT JOIN table_b b ON a.foreign_key = b.primary_key
            WHERE b.primary_key IS NULL
        """
    }
    
    # Acceptable thresholds:
    # - Null percentage < 20% for critical columns
    # - Date ranges within reasonable bounds
    # - <1% orphaned foreign key references
```

**Mitigation Strategy**:
- Add data quality warnings to query results
- Implement NULL handling in SQL generation
- Filter out invalid date ranges automatically
- Provide data quality dashboard for administrators
- Document known data quality issues in system

**Assumption Owner**: Data Team  
**Verification Deadline**: During initial schema load  
**Priority**: HIGH

---

### **A-3.3: Read-Only Access Sufficient for Use Cases**

**Assumption**: Users only need to read/query data, not insert, update, or delete records.

**Justification**:
- Project scope limited to data analysis and reporting
- Write operations require different security controls
- Healthcare data modification requires audit trails
- Separation of concerns: BI tool vs transactional system

**Impact if Correct**:
✅ Simplified security model  
✅ No risk of data corruption  
✅ Easier to validate generated SQL  
✅ Reduced compliance burden  

**Risk if Incorrect**:
❌ **Critical Impact** - Feature gap for users  
❌ Need complete rewrite of security model  
❌ Requires extensive testing and validation  
❌ HIPAA audit implications for data modifications  

**Validation Method**:
- Requirements validation: "Do you need to update data through this system?"
- User interviews: Document all use cases
- Access pattern analysis: Review current BI tool usage
- Compliance review: Data modification audit requirements

**Mitigation Strategy**:
- Phase 2 feature: Write operations with approval workflow
- Integration with existing transactional systems for updates
- Export to Excel for user-side modifications
- Clear documentation: "This is a read-only reporting tool"

**Assumption Owner**: Product Team  
**Verification Deadline**: Requirements phase  
**Priority**: CRITICAL (validate early)

---

### **A-3.4: Database Contains Sufficient Sample Data for Each Column**

**Assumption**: Most columns have enough diverse data values to provide meaningful examples for the LLM context.

**Justification**:
- Production databases typically have substantial data volume
- Sample values help LLM understand data patterns
- Examples improve SQL generation accuracy
- Healthcare databases accumulate years of data

**Impact if Correct**:
✅ Better context for LLM prompts  
✅ More accurate SQL generation  
✅ Helpful examples for users  
✅ Data type inference improved  

**Risk if Incorrect**:
❌ **Low Impact** - LLM has less context  
❌ May generate less precise SQL  
❌ Need fallback to data type only  
❌ Reduced accuracy for enum-like columns  

**Validation Method**:
```sql
-- Check data diversity for key columns
SELECT 
    table_name,
    column_name,
    COUNT(DISTINCT column_value) as distinct_values,
    COUNT(*) as total_values,
    CAST(COUNT(DISTINCT column_value) AS FLOAT) / COUNT(*) as diversity_ratio
FROM (
    -- Sample 10,000 rows per table
    SELECT TOP 10000 * FROM table_name
) sample
GROUP BY table_name, column_name
HAVING COUNT(DISTINCT column_value) > 1;

-- Flag columns with low diversity (<3 distinct values)
```

**Mitigation Strategy**:
- Use data type and constraints when samples unavailable
- Generate synthetic examples for sparse columns
- Mark low-data columns in schema with warnings
- Request sample data from database administrators

**Assumption Owner**: Data Team  
**Verification Deadline**: Schema ingestion  
**Priority**: LOW

---

## **4. Organizational Context Assumptions**

### **A-4.1: Organization Has HIPAA Compliance Requirements**

**Assumption**: Organization must comply with HIPAA regulations for patient data protection.

**Justification**:
- Healthcare context implies HIPAA applicability
- Typical for US healthcare organizations
- User personas (operations managers, physicians) access PHI
- Database contains patient information

**Impact if Correct**:
✅ Security design appropriately strict  
✅ Local processing requirement justified  
✅ Audit logging comprehensive  
✅ Compliance-driven features valuable  

**Risk if Incorrect**:
❌ **Low Impact** - Over-engineering security not harmful  
❌ Some security features may be overkill  
❌ Could be more permissive in data handling  
❌ May have simpler deployment options  

**Validation Method**:
- Confirm with legal/compliance team
- Review organization's BAA (Business Associate Agreement)
- Check if organization is covered entity or business associate
- Review existing system security requirements

**Mitigation Strategy**:
- Make security features configurable (strict vs permissive mode)
- Document which features are HIPAA-specific
- Provide non-healthcare deployment option
- Maintain separate security configurations

**Assumption Owner**: Compliance Team  
**Verification Deadline**: Project kickoff  
**Priority**: HIGH

---

### **A-4.2: IT Department Supports Open Source Tools**

**Assumption**: Organization allows deployment of open-source software (Python, Ollama, ChromaDB) in production.

**Justification**:
- Modern healthcare IT increasingly embraces open source
- Python widely accepted in enterprise environments
- Open source reduces licensing costs
- Similar tools already deployed in organization

**Impact if Correct**:
✅ No licensing obstacles  
✅ Cost savings vs commercial alternatives  
✅ Full control over deployment  
✅ Community support available  

**Risk if Incorrect**:
❌ **Critical Impact** - Project may be blocked  
❌ Need commercial alternatives (expensive)  
❌ Potential project cancellation  
❌ Extensive vendor evaluation process  

**Validation Method**:
- Review organization's software approval process
- Check list of pre-approved open source licenses (MIT, Apache 2.0)
- Identify precedents (other Python/OSS projects)
- Early security review of dependencies

**Mitigation Strategy**:
- **Immediate**: Get pre-approval from IT leadership
- Provide security assessment of all OSS components
- Document support options (commercial vs community)
- Identify commercial alternatives (Azure OpenAI, AWS Bedrock)
- Containerize to simplify deployment/security review

**Assumption Owner**: IT Leadership  
**Verification Deadline**: Before development starts  
**Priority**: CRITICAL

---

### **A-4.3: Users Have Windows or Linux Workstations**

**Assumption**: End users access system via web browser on Windows or Linux (not exclusively mobile/tablet).

**Justification**:
- Healthcare clinical/administrative staff use desktop computers
- Complex data analysis better suited for larger screens
- Web-based UI accessible from any modern browser
- Mobile use case secondary to desktop

**Impact if Correct**:
✅ UI design optimized for desktop  
✅ No need for native mobile apps  
✅ Simplified testing matrix  
✅ Better user experience for data analysis  

**Risk if Incorrect**:
❌ **Medium Impact** - Mobile users underserved  
❌ Need responsive design investment  
❌ Mobile-specific features required  
❌ Potential accessibility issues  

**Validation Method**:
- Survey users: "What device do you primarily use for data analysis?"
- Analytics from existing BI tools: Desktop vs mobile usage
- IT asset inventory: Desktop/laptop vs mobile device counts
- Use case analysis: Tasks requiring mobile vs desktop

**Mitigation Strategy**:
- Implement responsive design (already planned)
- Provide basic mobile functionality (query submission, view results)
- Phase 2: Native mobile app if demand exists
- Progressive web app (PWA) for offline mobile access

**Assumption Owner**: Product Team  
**Verification Deadline**: Design phase  
**Priority**: MEDIUM

---

### **A-4.4: Single Database Initially, Multi-Database Later**

**Assumption**: Phase 1 connects to one SQL Server database; multi-database support is Phase 2/3 enhancement.

**Justification**:
- Reduces initial complexity and development time
- Most organizations have primary data warehouse
- Cross-database queries less common initially
- Incremental feature development approach

**Impact if Correct**:
✅ Faster time to market  
✅ Simpler architecture initially  
✅ Focus on core functionality  
✅ Easier testing and validation  

**Risk if Incorrect**:
❌ **Medium Impact** - Users need multi-DB from day 1  
❌ Architectural changes required  
❌ User disappointment if expectation set incorrectly  
❌ Competitive disadvantage  

**Validation Method**:
- User research: "How many databases do you query regularly?"
- Access pattern analysis: Cross-database query frequency
- Requirements workshop: Prioritize single vs multi-DB
- MVP definition: Core features vs nice-to-have

**Mitigation Strategy**:
- Design abstraction layer for multi-database support
- Document multi-database as roadmap item
- Allow database switching in UI (one at a time)
- Provide federation layer as alternative (external tool)

**Assumption Owner**: Product Team  
**Verification Deadline**: Requirements definition  
**Priority**: MEDIUM

---

## **5. Resource Availability Assumptions**

### **A-5.1: Dedicated Development Team for 3-6 Months**

**Assumption**: Project has committed team of 2-3 developers for initial development phase (3-6 months).

**Justification**:
- Realistic timeline for MVP based on feature scope
- SPARC methodology requires iterative development
- Similar projects require 4-6 person-months effort
- Includes development, testing, documentation, deployment

**Impact if Correct**:
✅ Adequate resources for quality delivery  
✅ Iterative development cycles possible  
✅ Time for testing and refinement  
✅ Proper documentation and knowledge transfer  

**Risk if Incorrect**:
❌ **High Impact** - Project delayed or quality compromised  
❌ Technical debt accumulates  
❌ Insufficient testing leads to bugs  
❌ Poor documentation affects maintainability  

**Validation Method**:
- Resource allocation confirmation from management
- Team availability calendar review
- Competing project priorities assessment
- Staffing plan with named individuals

**Mitigation Strategy**:
- **Immediate**: Get written commitment for resources
- Identify critical path tasks requiring specific expertise
- Plan for part-time contributors if needed
- Outsource non-core components (UI design, testing)
- Reduce scope if resources unavailable

**Assumption Owner**: Project Manager  
**Verification Deadline**: Project kickoff  
**Priority**: CRITICAL

---

### **A-5.2: Access to Subject Matter Experts**

**Assumption**: Healthcare domain experts and database administrators available for consultation during development.

**Justification**:
- Need business logic validation for SQL generation
- Database schema understanding requires DBA input
- User testing requires domain expert participation
- Query validation needs healthcare knowledge

**Impact if Correct**:
✅ Accurate SQL generation for domain queries  
✅ Proper schema interpretation  
✅ Validated use cases and examples  
✅ User acceptance criteria defined correctly  

**Risk if Incorrect**:
❌ **High Impact** - System generates incorrect queries  
❌ Poor user experience due to misunderstanding needs  
❌ Deployment delays for requirement clarification  
❌ Expensive rework post-launch  

**Validation Method**:
- Identify SME stakeholders by name and role
- Schedule regular touchpoints (weekly/bi-weekly)
- Document required time commitment (4-8 hours/week)
- Get manager approval for SME participation

**Mitigation Strategy**:
- Front-load requirements gathering to minimize ongoing needs
- Record sessions for future reference
- Create comprehensive documentation to reduce future questions
- Hire external healthcare analytics consultant if needed

**Assumption Owner**: Product Team  
**Verification Deadline**: Requirements phase  
**Priority**: HIGH

---

### **A-5.3: Budget for Computational Resources**

**Assumption**: Organization budgets $5,000-10,000 for hardware/infrastructure (if not using existing servers).

**Justification**:
- Server hardware: $3,000-5,000
- Development workstations: $2,000-3,000
- Backup/DR infrastructure: $1,000-2,000
- Alternatively, cloud costs ~$500-1000/month

**Impact if Correct**:
✅ Adequate infrastructure for production deployment  
✅ Development and testing environments available  
✅ Disaster recovery capability  
✅ Performance targets achievable  

**Risk if Incorrect**:
❌ **Medium Impact** - Must use existing infrastructure  
❌ Resource contention with other systems  
❌ Performance compromises  
❌ No dedicated testing environment  

**Validation Method**:
- Budget approval documentation
- Purchase order or cloud account setup
- Infrastructure plan reviewed by finance
- Cost-benefit analysis presented to stakeholders

**Mitigation Strategy**:
- Leverage existing infrastructure if available
- Start with developer workstations for MVP
- Use free cloud tier for development/testing
- Containerize for flexible deployment options
- Phase infrastructure investment with project milestones

**Assumption Owner**: Finance/IT  
**Verification Deadline**: Before hardware procurement  
**Priority**: MEDIUM

---

## **6. Security and Compliance Assumptions**

### **A-6.1: Network Security Already Established**

**Assumption**: Organization has firewall, network segmentation, and VPN infrastructure in place.

**Justification**:
- Healthcare organizations typically have mature security
- HIPAA requires network security controls
- Not in scope to build network infrastructure
- Application-level security is project focus

**Impact if Correct**:
✅ Can focus on application security  
✅ No need to design network architecture  
✅ Faster deployment timeline  
✅ Leverages existing security investments  

**Risk if Incorrect**:
❌ **Critical Impact** - Cannot deploy securely  
❌ Project blocked pending infrastructure  
❌ Major cost increase for network setup  
❌ Timeline extended by months  

**Validation Method**:
- Network security assessment review
- Confirm firewall rules allow application traffic
- VPN access for remote users verified
- Network segmentation plan documented

**Mitigation Strategy**:
- Deploy in DMZ or secure zone with existing controls
- Use VPN for all remote access
- Implement application-level encryption as backup
- Cloud deployment as alternative (Azure/AWS security)

**Assumption Owner**: Security Team  
**Verification Deadline**: Deployment planning  
**Priority**: HIGH

---

### **A-6.2: Single Sign-On (SSO) Available**

**Assumption**: Organization has SSO infrastructure (SAML/OAuth2/LDAP) for authentication.

**Justification**:
- Modern healthcare organizations use SSO
- Reduces password management burden
- Better security than local accounts
- User convenience and adoption

**Impact if Correct**:
✅ Seamless user authentication  
✅ No password management needed  
✅ Centralized access control  
✅ Better security posture  

**Risk if Incorrect**:
❌ **Medium Impact** - Must implement local auth  
❌ Additional development effort (2-3 weeks)  
❌ Password reset and management complexity  
❌ Security audit requirements increase  

**Validation Method**:
- Confirm SSO provider (Azure AD, Okta, etc.)
- Test SSO integration in development
- Document SSO configuration requirements
- Get SSO admin support committed

**Mitigation Strategy**:
- Implement local authentication as fallback
- Use OAuth2 with popular providers (Google, Microsoft)
- Document both SSO and local auth setup
- Make authentication provider pluggable

**Assumption Owner**: IT Security  
**Verification Deadline**: Authentication implementation  
**Priority**: MEDIUM

---

### **A-6.3: Audit Logging Infrastructure Exists**

**Assumption**: Organization has centralized logging infrastructure (ELK, Splunk, etc.) for security audit logs.

**Justification**:
- HIPAA requires audit logging
- Enterprise security monitoring standard practice
- Integration easier than building from scratch
- Leverages existing security operations

**Impact if Correct**:
✅ Logs integrated with existing SIEM  
✅ Security team can monitor system  
✅ Compliance requirement satisfied  
✅ Incident response capabilities  

**Risk if Incorrect**:
❌ **High Impact** - Must build logging infrastructure  
❌ Compliance gap until resolved  
❌ Additional costs and complexity  
❌ Security monitoring delayed  

**Validation Method**:
- Identify logging infrastructure (ELK, Splunk, CloudWatch)
- Confirm log ingestion format and protocol
- Test log delivery in development
- Review retention and backup policies

**Mitigation Strategy**:
- Implement local file-based logging as fallback
- Use structured JSON logs for easy parsing
- Provide log shipping configuration for common platforms
- Document manual log review procedures

**Assumption Owner**: Security Team  
**Verification Deadline**: Security review  
**Priority**: HIGH

---

## **7. Integration and Dependency Assumptions**

### **A-7.1: Internet Access for Ollama Model Downloads**

**Assumption**: Installation/setup environment has temporary internet access for downloading LLM models (5-10GB).

**Justification**:
- Models downloaded once during setup
- Standard practice for ML model deployment
- Alternative is manual model transfer (complex)
- Internet access common during provisioning

**Impact if Correct**:
✅ Simple model installation process  
✅ Easy updates to newer model versions  
✅ Standard deployment procedure  
✅ Reduced manual effort  

**Risk if Incorrect**:
❌ **Medium Impact** - Manual model transfer required  
❌ Slower deployment process  
❌ Version management complexity  
❌ Documentation more complex  

**Validation Method**:
- Confirm network policy allows outbound HTTPS
- Test download from ollama.ai during setup
- Verify firewall allows temporary access
- Document offline installation procedure

**Mitigation Strategy**:
- Download models on internet-connected machine
- Transfer via USB/secure file transfer
- Provide pre-packaged model files
- Document offline installation process
- Create internal model repository if needed

**Assumption Owner**: IT Network  
**Verification Deadline**: Installation planning  
**Priority**: MEDIUM

---

### **A-7.2: No External API Dependencies**

**Assumption**: System operates without requiring external API calls (Google, OpenAI, etc.) after initial setup.

**Justification**:
- Core requirement: local processing for privacy
- HIPAA compliance concerns with external APIs
- Network isolation requirement
- Cost control (no per-query charges)

**Impact if Correct**:
✅ Full data privacy maintained  
✅ No external service dependencies  
✅ Predictable costs  
✅ Works in air-gapped environments  

**Risk if Incorrect**:
❌ **Critical Impact** - Privacy requirements violated  
❌ Cannot deploy in secure environments  
❌ HIPAA compliance at risk  
❌ Ongoing API costs  

**Validation Method**:
- Code audit: No external API calls in production code
- Network traffic monitoring: Verify no outbound connections
- Security review: Confirm local-only operation
- Compliance verification: Data never leaves environment

**Mitigation Strategy**:
- This is a hard requirement; no mitigation needed
- Design must maintain local-only operation
- Any future external integration requires approval
- Clearly document local-only architecture

**Assumption Owner**: Compliance Team  
**Verification Deadline**: Architecture review  
**Priority**: CRITICAL

---

### **A-7.3: Python Ecosystem Stability**

**Assumption**: Key Python dependencies (LangChain, ChromaDB, Streamlit) remain stable and backward-compatible.

**Justification**:
- Mature libraries with established APIs
- Semantic versioning practices
- Active maintenance and community
- Enterprise adoption indicates stability

**Impact if Correct**:
✅ Smooth dependency updates  
✅ Security patches without breaking changes  
✅ Long-term maintainability  
✅ Community support available  

**Risk if Incorrect**:
❌ **Medium Impact** - Breaking changes require rework  
❌ Security vulnerabilities in unmaintained packages  
❌ Forced migration to alternatives  
❌ Maintenance burden increases  

**Validation Method**:
- Monitor dependency changelogs
- Subscribe to security advisories
- Test dependency updates in staging
- Track deprecation warnings

**Mitigation Strategy**:
- Pin dependency versions in requirements.txt
- Regular dependency updates with testing
- Abstract dependencies behind interfaces
- Maintain compatibility matrix
- Have alternative libraries identified

**Assumption Owner**: Development Team  
**Verification Deadline**: Ongoing  
**Priority**: MEDIUM

---

## **8. Performance and Scale Assumptions**

### **A-8.1: 10-20 Concurrent Users Maximum**

**Assumption**: Peak usage will not exceed 10-20 simultaneous active users.

**Justification**:
- Initial deployment to single department/unit
- Healthcare analytics tools typically have modest concurrency
- Not public-facing application
- Usage patterns show sequential rather than simultaneous use

**Impact if Correct**:
✅ Architecture appropriately scaled  
✅ Hardware requirements realistic  
✅ No need for complex load balancing  
✅ Cost-effective deployment  

**Risk if Incorrect**:
❌ **High Impact** - Performance degradation under load  
❌ User experience suffers  
❌ Need architectural changes for scale  
❌ Additional infrastructure costs  

**Validation Method**:
```python
# Load testing
def load_test_concurrent_users():
    from locust import HttpUser, task, between
    
    class QueryUser(HttpUser):
        wait_time = between(1, 3)
        
        @task
        def submit_query(self):
            self.client.post("/api/query", json={
                "query": "How many patients admitted yesterday?"
            })
    
    # Test with 10, 20, 30, 50 concurrent users
    # Measure:
    # - Response time at each level
    # - Error rate
    # - System resource usage
    
    # Success criteria:
    # - <5s response at 20 users
    # - <1% error rate at 20 users
```

**Mitigation Strategy**:
- Implement request queuing for overflow
- Horizontal scaling plan (multiple instances)
- Cache query results for popular queries
- Rate limiting per user (e.g., 10 queries/minute)
- Cloud deployment with auto-scaling if needed

**Assumption Owner**: Architecture Team  
**Verification Deadline**: Load testing phase  
**Priority**: HIGH

---

### **A-8.2: Database Has <1000 Tables**

**Assumption**: Target database contains fewer than 1000 tables to index in vector store.

**Justification**:
- Typical healthcare data warehouse: 200-500 tables
- Schema complexity manageable at this scale
- Vector store performance acceptable
- RAG retrieval remains fast

**Impact if Correct**:
✅ Vector store indexing completes quickly (<10 minutes)  
✅ RAG retrieval fast (<500ms)  
✅ Schema browser remains usable  
✅ Memory requirements reasonable  

**Risk if Incorrect**:
❌ **Medium Impact** - Slow indexing and retrieval  
❌ Need optimization for large schemas  
❌ UI becomes overwhelming  
❌ Memory usage higher than expected  

**Validation Method**:
```sql
-- Count tables in database
SELECT 
    s.name as schema_name,
    COUNT(*) as table_count
FROM sys.tables t
JOIN sys.schemas s ON t.schema_id = s.schema_id
GROUP BY s.name
ORDER BY table_count DESC;

-- Total count
SELECT COUNT(*) as total_tables FROM sys.tables;
```

**Mitigation Strategy**:
- Hierarchical indexing for large schemas
- Schema filtering (exclude system/temp tables)
- Paginated schema browser
- Search-based schema navigation
- Optimize vector store with HNSW indexing

**Assumption Owner**: Data Team  
**Verification Deadline**: Schema discovery  
**Priority**: MEDIUM

---

### **A-8.3: Queries Return <10,000 Rows Typically**

**Assumption**: Most queries return manageable result sets (<10,000 rows), not millions.

**Justification**:
- Analytical queries typically aggregate data
- Users exploring data, not bulk exporting
- UI designed for human-readable results
- Large exports should use dedicated ETL tools

**Impact if Correct**:
✅ Result formatting performant  
✅ UI remains responsive  
✅ Network transfer reasonable  
✅ Browser memory sufficient  

**Risk if Incorrect**:
❌ **Medium Impact** - UI freezes or crashes  
❌ Network timeouts  
❌ Poor user experience  
❌ Browser tab crashes  

**Validation Method**:
- Analyze existing query patterns in current BI tool
- Monitor row counts in production logs
- Test UI with large result sets (10K, 50K, 100K rows)
- Measure performance degradation

**Mitigation Strategy**:
- Enforce maximum row limit (10,000 by default)
- Pagination for large results
- Streaming results for better UX
- Suggest aggregation for large datasets
- Export to file for large results instead of display

**Assumption Owner**: Product Team  
**Verification Deadline**: UI testing  
**Priority**: MEDIUM

---

## **9. Assumption Summary Matrix**

| ID | Assumption | Priority | Risk | Validation Status |
|----|------------|----------|------|------------------|
| A-1.1 | Adequate hardware (16GB RAM, 8 cores) | CRITICAL | High | ⏳ Pre-deployment |
| A-1.2 | Local database network access | HIGH | Medium | ⏳ Setup phase |
| A-1.3 | Ollama runs reliably | CRITICAL | Critical | ⏳ Initial setup |
| A-1.4 | CPU-only acceptable performance | HIGH | Medium | ⏳ Benchmarking |
| A-2.1 | Users lack SQL knowledge | MEDIUM | Low | ⏳ User research |
| A-2.2 | Users know healthcare terms | MEDIUM | Medium | ⏳ User testing |
| A-2.3 | 3-5s response acceptable | HIGH | High | ⏳ UAT |
| A-2.4 | Conversational follow-up preferred | MEDIUM | Low | ⏳ Beta testing |
| A-3.1 | Schema relatively stable | MEDIUM | Medium | ⏳ First month |
| A-3.2 | Data quality consistent | HIGH | High | ⏳ Schema load |
| A-3.3 | Read-only access sufficient | CRITICAL | Critical | ✅ Validated |
| A-3.4 | Sufficient sample data | LOW | Low | ⏳ Schema load |
| A-4.1 | HIPAA compliance required | HIGH | Low | ⏳ Kickoff |
| A-4.2 | Open source allowed | CRITICAL | Critical | ⚠️ Urgent |
| A-4.3 | Desktop workstations | MEDIUM | Medium | ⏳ Design phase |
| A-4.4 | Single database initially | MEDIUM | Medium | ✅ Validated |
| A-5.1 | Dedicated team (3-6 months) | CRITICAL | High | ⏳ Kickoff |
| A-5.2 | SME access available | HIGH | High | ⏳ Requirements |
| A-5.3 | Infrastructure budget | MEDIUM | Medium | ⏳ Procurement |
| A-6.1 | Network security in place | HIGH | Critical | ⏳ Deploy planning |
| A-6.2 | SSO available | MEDIUM | Medium | ⏳ Auth implementation |
| A-6.3 | Logging infrastructure exists | HIGH | High | ⏳ Security review |
| A-7.1 | Internet for model downloads | MEDIUM | Medium | ⏳ Install planning |
| A-7.2 | No external API dependencies | CRITICAL | Critical | ✅ Validated |
| A-7.3 | Python ecosystem stable | MEDIUM | Medium | 🔄 Ongoing |
| A-8.1 | 10-20 concurrent users | HIGH | High | ⏳ Load testing |
| A-8.2 | <1000 tables in database | MEDIUM | Medium | ⏳ Schema discovery |
| A-8.3 | <10K rows per query | MEDIUM | Medium | ⏳ UI testing |

**Legend**:
- ✅ Validated - Assumption confirmed
- ⏳ Pending - Awaiting validation
- ⚠️ Urgent - Needs immediate attention
- 🔄 Ongoing - Continuous monitoring
- ❌ Invalidated - Assumption proven false

---

## **10. Assumption Management Process**

### **Ownership and Accountability**

Each assumption has a designated owner responsible for:
- Validating the assumption
- Monitoring changes that affect validity
- Updating stakeholders if assumption proves false
- Executing mitigation strategy if needed

### **Validation Cadence**

- **CRITICAL assumptions**: Validate before project start
- **HIGH priority**: Validate during relevant phase
- **MEDIUM priority**: Validate during implementation
- **LOW priority**: Validate opportunistically

### **Change Management**

When an assumption is invalidated:

1. **Assess Impact**: Determine effect on timeline, budget, scope
2. **Notify Stakeholders**: Communicate changes immediately
3. **Activate Mitigation**: Execute planned mitigation strategy
4. **Update Documentation**: Revise affected specifications
5. **Adjust Plan**: Update project plan and estimates
6. **Lessons Learned**: Document for future projects

### **Regular Review**

Assumptions reviewed at:
- Project kickoff
- End of each development sprint
- Major milestone completions
- Quarterly for long projects
- When significant changes occur

---

## **11. Key Takeaways**

**Most Critical Assumptions** (Must validate immediately):
1. **A-1.3**: Ollama runs reliably (core technology choice)
2. **A-4.2**: Open source tools allowed (legal/policy blocker)
3. **A-5.1**: Team resources available (project feasibility)
4. **A-7.2**: No external dependencies (architecture foundation)
5. **A-3.3**: Read-only sufficient (scope definition)

**Highest Risk Assumptions** (Most likely to be wrong):
1. **A-1.1**: Hardware resources adequate (often underestimated)
2. **A-2.3**: Response time acceptable (user expectations vary)
3. **A-3.2**: Data quality consistent (common issue in real databases)
4. **A-8.1**: Concurrent user count (usage often exceeds estimates)

**Assumptions with Good Mitigation**:
- Technical assumptions generally have clear alternatives
- Resource constraints can be addressed with scope reduction
- Performance issues addressable through optimization
- Security/compliance assumptions backed by standards

**Assumptions Needing Better Mitigation**:
- **A-4.2** (Open source approval): No good alternative
- **A-5.1** (Team resources): Project fails without adequate staffing
- **A-6.1** (Network security): Cannot deploy without infrastructure

The success of this project depends heavily on validating critical assumptions early and maintaining flexibility to adapt when assumptions prove incorrect.