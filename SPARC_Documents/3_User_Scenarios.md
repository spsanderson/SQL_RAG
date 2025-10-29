# **User Scenarios and User Flows: Local LLM RAG SQL Query Application**

---
[Back to Main SPARC Documentation](SQL%20LLM%20RAG%20Project%20SPARC.md)

## **Overview**

User scenarios describe realistic situations where users interact with the system to accomplish specific goals. User flows map the step-by-step paths users take through the interface, including decision points, alternative paths, and error handling. These scenarios inform design decisions, testing strategies, and feature prioritization.

---

## **Scenario 1: Daily Operations Report (Simple Query)**

### **User Persona**: Sarah - Clinical Operations Manager

**Context**: Sarah arrives at work at 8:00 AM and needs to prepare yesterday's discharge statistics for the morning leadership meeting at 8:30 AM.

**User Goals**:
- Obtain accurate discharge count from previous day
- Understand discharge patterns (e.g., by unit, disposition)
- Complete task in under 5 minutes
- Export results for presentation

**Preconditions**:
- Sarah is logged into the application
- Database contains up-to-date discharge data
- Sarah has SELECT permissions on patient accounting tables

**User Knowledge Level**: Beginner - knows what data she needs but no SQL knowledge

---

### **Primary Flow: Successful Query Execution**

#### **Step-by-Step Interaction**

**Step 1: Application Landing**
- **User Action**: Sarah opens the application URL in Chrome
- **System Response**: 
  - Displays login page (if not authenticated)
  - After SSO authentication, shows main query interface
  - Query input box is auto-focused
  - History sidebar shows her last 5 queries from previous days
- **UI State**: Clean interface, example queries visible in dropdown

**Step 2: Query Input**
- **User Action**: Sarah types in the query input box:
  ```
  "How many inpatient accounts were discharged yesterday?"
  ```
- **System Response**:
  - Character counter shows "52/500 characters"
  - Autocomplete dropdown suggests similar past queries:
    - "How many inpatient discharges yesterday?"
    - "Discharge count by day"
  - No autocomplete selected; Sarah continues typing
- **Decision Point**: User can either:
  - Continue typing original query
  - Select an autocomplete suggestion
  - Click example query from sidebar

**Step 3: Query Submission**
- **User Action**: Sarah presses Enter key (or clicks Submit button)
- **System Response**:
  - Submit button becomes disabled
  - Loading spinner appears with text: "Understanding your question..."
  - Query input box is locked (can't edit during processing)
  - Estimated time appears: "Usually takes 3-5 seconds"
- **UI State**: Clear visual feedback that system is working

**Step 4: Intent Classification and Validation (Background)**
- **System Processing**:
  - Parses query intent: COUNT operation, single table, date filter
  - Identifies entities: "inpatient", "discharged", "yesterday"
  - Validates query is not ambiguous
  - Confidence score: 0.92 (high confidence)
- **Decision Point**: 
  - If confidence < 0.7: Ask clarifying question
  - If confidence ≥ 0.7: Proceed to RAG retrieval

**Step 5: RAG Context Retrieval (Background)**
- **System Processing**:
  - Generates embedding for user query
  - Searches vector store for relevant schema
  - Retrieves:
    - `pt_accounting_reporting_alt` table schema
    - Column definitions for `acct_type`, `dsch_date`
    - Similar past queries with date logic
    - Business rule: "IP" = Inpatient
  - Top 3 relevant contexts selected
  - Total context: 1,200 tokens
- **System State**: Context ready for LLM prompt construction

**Step 6: SQL Generation via LLM (Background)**
- **System Processing**:
  - Constructs prompt with schema + examples + user query
  - Sends to Ollama (SQLCoder-7B model)
  - Loading message updates: "Generating SQL query..."
  - LLM responds in 2.3 seconds with SQL:
    ```sql
    SELECT COUNT(*) 
    FROM sms.dbo.pt_accounting_reporting_alt 
    WHERE acct_type = 'IP' 
      AND dsch_date = DATEADD(day, -1, CAST(GETDATE() AS DATE))
    ```
  - Parses SQL from response, removes markdown formatting

**Step 7: SQL Validation (Background)**
- **System Processing**:
  - Checks for prohibited operations (DROP, DELETE, etc.) - PASS
  - Validates table exists in schema - PASS
  - Verifies columns exist - PASS
  - Confirms read-only operation - PASS
  - Complexity check: Simple query - PASS
- **Decision Point**:
  - If validation fails: Show error, retry with corrected prompt
  - If validation passes: Proceed to execution

**Step 8: Query Execution (Background)**
- **System Processing**:
  - Acquires database connection from pool (23ms)
  - Loading message updates: "Executing query..."
  - Executes SQL with 30-second timeout
  - Query completes in 0.8 seconds
  - Result: Single row, single column: 45
  - Logs query execution: user, timestamp, SQL, row count

**Step 9: Results Display**
- **System Response**:
  - Loading spinner disappears
  - Results section animates into view
  - **SQL Query Display** (collapsible, expanded by default):
    ```sql
    SELECT COUNT(*) 
    FROM sms.dbo.pt_accounting_reporting_alt 
    WHERE acct_type = 'IP' 
      AND dsch_date = DATEADD(day, -1, CAST(GETDATE() AS DATE))
    ```
    - Syntax highlighted
    - Copy button in top-right corner
  
  - **Natural Language Answer** (prominent):
    > **45 inpatient accounts** were discharged yesterday.
  
  - **Data Table** (for this query, single value):
    | COUNT(*) |
    |----------|
    | 45       |
  
  - **Query Metadata**:
    - Execution time: 0.8 seconds
    - Rows returned: 1
    - Query timestamp: 2025-10-29 08:05:23
  
  - **Action Buttons**:
    - [Export to CSV] [Export to Excel] [Copy SQL] [Save Query]

- **UI State**: Success state with green checkmark icon

**Step 10: Query Saved to History**
- **System Processing**:
  - Adds query to user's session history
  - Saves to history sidebar (top of list)
  - Marks as successful query
  - Updates query count in profile

**Step 11: Follow-Up Query**
- **User Action**: Sarah wants more detail, types:
  ```
  "Show me the breakdown by discharge disposition"
  ```
- **System Response**:
  - Recognizes this as follow-up to previous query
  - Retrieves conversation context (previous SQL)
  - Loading spinner with message: "Refining previous query..."

**Step 12: Context-Aware SQL Generation**
- **System Processing**:
  - Prompt includes previous SQL as context
  - Instruction: "Modify to add GROUP BY dsch_disp"
  - LLM generates modified SQL:
    ```sql
    SELECT dsch_disp, COUNT(*) as discharge_count
    FROM sms.dbo.pt_accounting_reporting_alt 
    WHERE acct_type = 'IP' 
      AND dsch_date = DATEADD(day, -1, CAST(GETDATE() AS DATE))
    GROUP BY dsch_disp
    ORDER BY discharge_count DESC
    ```

**Step 13: Grouped Results Display**
- **System Response**:
  - Shows natural language summary:
    > Yesterday's 45 inpatient discharges by disposition:
  
  - **Data Table**:
    | Discharge Disposition | Discharge Count |
    |----------------------|-----------------|
    | Home                 | 28              |
    | Skilled Nursing      | 10              |
    | Home Health          | 5               |
    | Rehab Facility       | 2               |
  
  - Export buttons available
  - Pagination controls (not needed for 4 rows)

**Step 14: Export Results**
- **User Action**: Sarah clicks [Export to Excel]
- **System Response**:
  - Generates XLSX file with:
    - Results on Sheet 1
    - SQL query on Sheet 2 (for reference)
    - Metadata (timestamp, user, query text)
  - Browser downloads file: `discharge_report_2025-10-29.xlsx`
  - Success message: "Report exported successfully"

**Step 15: Task Completion**
- **User Action**: Sarah reviews the exported file
- **Outcome**: 
  - ✅ Accurate data obtained in 4 minutes
  - ✅ Ready for leadership meeting
  - ✅ Can re-run same query tomorrow via history
- **User Satisfaction**: High - task completed quickly and easily

---

### **Flow Diagram: Successful Simple Query**

```
┌─────────────────────────────────────────────────────────────┐
│                     START: User Needs Data                  │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Open App URL  │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Login (SSO)   │
                    └────────┬───────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Main Query Screen   │
                 │  - Input box focused │
                 │  - History visible   │
                 └──────────┬───────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Type Query          │
                 │  "How many inpatient │
                 │  discharged yesterday"│
                 └──────────┬───────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Press Enter         │
                 │  (Submit Query)      │
                 └──────────┬───────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Loading Indicator   │
                 │  "Understanding..."  │
                 └──────────┬───────────┘
                             │
                   ┌─────────┴─────────┐
                   │   System Process   │
                   │   (Background)     │
                   │                    │
                   │  1. Parse Intent   │
                   │  2. RAG Retrieve   │
                   │  3. Generate SQL   │
                   │  4. Validate SQL   │
                   │  5. Execute Query  │
                   └─────────┬──────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Display Results     │
                 │  ┌────────────────┐  │
                 │  │ SQL (collapsible)│ │
                 │  ├────────────────┤  │
                 │  │ Answer: 45     │  │
                 │  ├────────────────┤  │
                 │  │ Data Table     │  │
                 │  ├────────────────┤  │
                 │  │ Export buttons │  │
                 │  └────────────────┘  │
                 └──────────┬───────────┘
                             │
                  ┌──────────┴──────────┐
                  │                     │
             User Satisfied?            │
                  │                     │
         ┌────────┴────────┐            │
         │ Yes             │ No         │
         ▼                 ▼            │
    ┌─────────┐     ┌──────────────┐   │
    │  Export │     │ Follow-up    │   │
    │ Results │     │ Query        │───┘
    └────┬────┘     └──────┬───────┘
         │                 │
         ▼                 ▼
    ┌─────────┐     ┌──────────────┐
    │ Download│     │ Type new     │
    │  File   │     │ question     │
    └────┬────┘     └──────┬───────┘
         │                 │
         │                 └──────┐
         │                        │
         ▼                        ▼
    ┌─────────────────────────────────┐
    │      Task Complete              │
    │  - Data obtained                │
    │  - Query saved to history       │
    │  - Ready for meeting            │
    └─────────────────────────────────┘
```

---

### **Alternative Flow 1A: Ambiguous Query Clarification**

**Trigger**: User query is vague or ambiguous (confidence < 0.7)

**Example Query**: "Show me discharges"

**Step 3a: Query Submission**
- User types: "Show me discharges"
- Presses Enter

**Step 4a: Low Confidence Detection**
- **System Processing**:
  - Intent classification confidence: 0.45 (low)
  - Ambiguous elements detected:
    - Time range not specified (today? yesterday? this week?)
    - Patient type not specified (all? inpatient only?)
    - Output format unclear (count? list? breakdown?)

**Step 5a: Clarification Request**
- **System Response**:
  - Pauses processing
  - Shows clarification dialog:
    ```
    ┌─────────────────────────────────────────┐
    │  I need a bit more information:        │
    │                                         │
    │  1. Which date range?                  │
    │     ○ Yesterday                        │
    │     ○ Last 7 days                      │
    │     ○ Last 30 days                     │
    │     ○ Custom range                     │
    │                                         │
    │  2. Which patient types?               │
    │     ☑ Inpatient                        │
    │     ☐ Outpatient                       │
    │     ☐ Emergency                        │
    │                                         │
    │  3. What information do you need?      │
    │     ○ Total count                      │
    │     ○ Breakdown by unit               │
    │     ○ Breakdown by disposition         │
    │                                         │
    │  [Continue]  [Rewrite Question]        │
    └─────────────────────────────────────────┘
    ```

**Step 6a: User Clarification**
- **User Action**: 
  - Selects: Yesterday
  - Checks: Inpatient
  - Selects: Total count
  - Clicks [Continue]

**Step 7a: Resume Processing**
- **System Response**:
  - Reconstructs query with clarifications
  - New interpreted query: "How many inpatient discharges yesterday?"
  - Proceeds with normal flow from Step 5 (RAG Retrieval)

**Outcome**: Successfully navigates ambiguity without frustrating user

---

### **Alternative Flow 1B: SQL Validation Failure**

**Trigger**: Generated SQL fails validation checks

**Step 7b: Validation Error Detected**
- **System Processing**:
  - LLM generates SQL with non-existent table:
    ```sql
    SELECT COUNT(*) FROM patient_discharges 
    WHERE discharge_date = GETDATE() - 1
    ```
  - Validation step checks schema: `patient_discharges` table not found
  - Validation FAILS

**Step 8b: Automatic Retry with Context**
- **System Response**:
  - Does NOT show error to user yet
  - Reformulates prompt with error context:
    ```
    Previous SQL failed: Table 'patient_discharges' does not exist.
    
    Available tables:
    - pt_accounting_reporting_alt (contains discharge data)
    - patient_master
    - encounters
    
    Please regenerate SQL using correct table name.
    ```
  - Sends corrected prompt to LLM
  - Loading message: "Refining query..."

**Step 9b: Corrected SQL Generation**
- **System Processing**:
  - LLM generates corrected SQL:
    ```sql
    SELECT COUNT(*) FROM sms.dbo.pt_accounting_reporting_alt
    WHERE acct_type = 'IP' 
      AND dsch_date = DATEADD(day, -1, CAST(GETDATE() AS DATE))
    ```
  - Validation passes
  - Proceeds with execution

**Outcome**: System self-corrects without user intervention

---

### **Alternative Flow 1C: Query Execution Timeout**

**Trigger**: Database query exceeds 30-second timeout

**Step 8c: Timeout Detected**
- **System Processing**:
  - Query running for 30+ seconds
  - Database connection timeout triggered
  - Exception caught: `QueryTimeout`

**Step 9c: Error Handling**
- **System Response**:
  - Cancels query execution
  - Rolls back transaction (if any)
  - Shows user-friendly error:
    ```
    ┌─────────────────────────────────────────┐
    │  ⚠️  Query Timeout                      │
    │                                         │
    │  Your query took too long to execute   │
    │  (> 30 seconds).                       │
    │                                         │
    │  Suggestions:                           │
    │  • Add date filters to limit data      │
    │  • Request aggregated data instead     │
    │    of detailed records                 │
    │  • Break into smaller queries          │
    │                                         │
    │  Generated SQL:                         │
    │  [Show SQL] (collapsible)              │
    │                                         │
    │  [Try Again]  [Simplify Query]         │
    └─────────────────────────────────────────┘
    ```

**Step 10c: User Decision**
- **User Action**: Clicks [Simplify Query]
- **System Response**:
  - Suggests simplified version:
    - "How many inpatient discharges yesterday?" → specific date
    - Instead of "Show all discharge details this year" → too broad

**Outcome**: User learns query optimization through helpful guidance

---

## **Scenario 2: Complex Analytical Query (Advanced User)**

### **User Persona**: Mark - Healthcare Data Analyst

**Context**: Mark needs to calculate 30-day readmission rates by service line for a quarterly quality report. This requires joining multiple tables and complex date logic.

**User Goals**:
- Calculate readmission rate with proper logic
- Group results by service line
- Verify SQL correctness before execution
- Export for further analysis in Excel

**Preconditions**:
- Mark is logged in with Analyst role
- Has used system for 3+ months (experienced user)
- Understands SQL and can review generated queries

**User Knowledge Level**: Advanced - knows SQL, uses system for complex queries

---

### **Primary Flow: Complex Multi-Table Query**

**Step 1: Query Input**
- **User Action**: Mark types complex request:
  ```
  "Calculate 30-day all-cause readmission rate by service line for Q3 2024. 
  Include initial admission count, readmission count, and rate percentage."
  ```

**Step 2: System Processing**
- **System Response**:
  - Recognizes complexity: Multiple metrics, time range, grouping
  - Loading message: "Processing complex query..."
  - Estimated time: "This may take 10-15 seconds"

**Step 3: RAG Retrieval (Enhanced)**
- **System Processing**:
  - Retrieves multiple tables:
    - `encounters` - admission data
    - `pt_accounting_reporting_alt` - discharge dates
    - `service_line_master` - service line definitions
  - Finds past readmission calculation logic from similar queries
  - Retrieves business rule: "30-day readmission = readmit within 30 days of discharge, excluding planned readmits"

**Step 4: Complex SQL Generation**
- **System Processing**:
  - Generates SQL with CTE (Common Table Expression):
    ```sql
    WITH initial_admits AS (
        SELECT 
            e.encounter_id,
            e.patient_id,
            e.admit_date,
            p.dsch_date,
            s.service_line
        FROM encounters e
        JOIN pt_accounting_reporting_alt p ON e.encounter_id = p.encounter_id
        JOIN service_line_master s ON e.service_line_id = s.service_line_id
        WHERE e.admit_date >= '2024-07-01' 
          AND e.admit_date < '2024-10-01'
          AND e.admit_type = 'Unplanned'
    ),
    readmits AS (
        SELECT 
            ia.encounter_id as initial_encounter_id,
            ia.patient_id,
            ia.service_line,
            COUNT(re.encounter_id) as readmit_count
        FROM initial_admits ia
        LEFT JOIN encounters re 
            ON ia.patient_id = re.patient_id
            AND re.admit_date > ia.dsch_date
            AND re.admit_date <= DATEADD(day, 30, ia.dsch_date)
            AND re.admit_type = 'Unplanned'
        GROUP BY ia.encounter_id, ia.patient_id, ia.service_line
    )
    SELECT 
        service_line,
        COUNT(DISTINCT initial_encounter_id) as initial_admissions,
        SUM(CASE WHEN readmit_count > 0 THEN 1 ELSE 0 END) as readmissions,
        CAST(SUM(CASE WHEN readmit_count > 0 THEN 1 ELSE 0 END) * 100.0 / 
             COUNT(DISTINCT initial_encounter_id) AS DECIMAL(5,2)) as readmit_rate_pct
    FROM readmits
    GROUP BY service_line
    ORDER BY readmit_rate_pct DESC
    ```

**Step 5: Query Preview (Complexity Warning)**
- **System Response**:
  - Shows preview dialog before execution:
    ```
    ┌─────────────────────────────────────────────────────┐
    │  ⚠️  Complex Query Detected                         │
    │                                                     │
    │  This query will:                                   │
    │  • Join 3 tables                                    │
    │  • Use Common Table Expressions (CTEs)              │
    │  • Process ~50,000 records                          │
    │  • Estimated execution time: 8-12 seconds           │
    │                                                     │
    │  Generated SQL:                                     │
    │  ┌─────────────────────────────────────────────┐   │
    │  │ WITH initial_admits AS (                    │   │
    │  │     SELECT e.encounter_id, ...              │   │
    │  │ [Expand to see full SQL]                    │   │
    │  └─────────────────────────────────────────────┘   │
    │                                                     │
    │  Options:                                           │
    │  [Review SQL] [Execute] [Modify Query] [Cancel]    │
    └─────────────────────────────────────────────────────┘
    ```

**Step 6: SQL Review**
- **User Action**: Mark clicks [Review SQL]
- **System Response**:
  - Opens full SQL in modal with syntax highlighting
  - Provides [Copy] and [Edit] buttons
  - Mark reviews the logic, sees it's correct

**Step 7: Execution Confirmation**
- **User Action**: Mark clicks [Execute]
- **System Response**:
  - Executes query with progress indicator
  - Shows execution stages:
    - "Processing initial admits CTE... ✓"
    - "Identifying readmissions... ✓"
    - "Calculating rates... ✓"
  - Query completes in 9.2 seconds

**Step 8: Results Display**
- **System Response**:
  - Natural language summary:
    > **Q3 2024 30-Day Readmission Rates by Service Line:**
    > Based on 3,847 initial admissions across 8 service lines.
  
  - **Data Table**:
    | Service Line | Initial Admissions | Readmissions | Readmit Rate % |
    |--------------|-------------------|--------------|----------------|
    | Cardiology   | 892               | 78           | 8.74           |
    | Orthopedics  | 645               | 42           | 6.51           |
    | General Surgery | 523            | 31           | 5.93           |
    | Neurology    | 418               | 23           | 5.50           |
    | Oncology     | 387               | 18           | 4.65           |
    | Pulmonary    | 356               | 14           | 3.93           |
    | Gastro       | 334               | 11           | 3.29           |
    | Nephrology   | 292               | 8            | 2.74           |
  
  - **Query Metadata**:
    - Execution time: 9.2 seconds
    - Rows returned: 8
    - Complexity: High
  
  - **Additional Actions**:
    - [Export to Excel] [Save as Template] [Schedule Report]

**Step 9: Save as Template**
- **User Action**: Mark clicks [Save as Template]
- **System Response**:
  - Opens template dialog:
    ```
    ┌─────────────────────────────────────────┐
    │  Save Query as Template                 │
    │                                         │
    │  Template Name:                         │
    │  [30-Day Readmission Rate by Service Line] │
    │                                         │
    │  Parameters (make dynamic):             │
    │  ☑ Date Range (currently Q3 2024)      │
    │  ☐ Service Line (currently all)        │
    │  ☐ Admit Type (currently Unplanned)    │
    │                                         │
    │  Share with:                            │
    │  ○ Just me                              │
    │  ● My team                              │
    │  ○ Entire organization                  │
    │                                         │
    │  [Save Template]  [Cancel]              │
    └─────────────────────────────────────────┘
    ```
  - Mark configures template with dynamic date range
  - Clicks [Save Template]

**Step 10: Template Saved**
- **System Response**:
  - Success message: "Template saved successfully"
  - Template appears in sidebar under "My Templates"
  - Team members can now reuse this query pattern

**Outcome**: Complex analytical query completed successfully, reusable for future reports

---

### **Flow Diagram: Complex Analytical Query**

```
┌─────────────────────────────────────────────────────────────┐
│       START: Analyst Needs Complex Calculation             │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Type Complex Query  │
                 │  "Calculate 30-day   │
                 │  readmission rate    │
                 │  by service line..."  │
                 └──────────┬───────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Submit Query        │
                 └──────────┬───────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  System Detects      │
                 │  Complexity          │
                 │  (Multi-table JOIN)  │
                 └──────────┬───────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Enhanced RAG        │
                 │  Retrieval           │
                 │  • 3 tables          │
                 │  • Past calculations │
                 │  • Business rules    │
                 └──────────┬───────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Generate Complex    │
                 │  SQL with CTEs       │
                 └──────────┬───────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Show Preview Dialog │
                 │  ⚠️ Complex Query    │
                 │  • Table count       │
                 │  • Est. time         │
                 │  [Review] [Execute]  │
                 └──────────┬───────────┘
                             │
                  ┌──────────┴──────────┐
                  │                     │
            [Review SQL]          [Execute Now]
                  │                     │
                  ▼                     │
         ┌────────────────┐             │
         │ SQL Modal      │             │
         │ • Syntax       │             │
         │   highlight    │             │
         │ • Copy/Edit    │             │
         │ [Execute]      │             │
         └────────┬───────┘             │
                  │                     │
                  └──────────┬──────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Execute Query       │
                 │  Progress Indicator: │
                 │  • CTE 1... ✓        │
                 │  • CTE 2... ✓        │
                 │  • Final calc... ✓   │
                 └──────────┬───────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │  Display Results     │
                 │  • Summary stats     │
                 │  • 8-row table       │
                 │  • Metadata          │
                 │  [Export] [Save]     │
                 └──────────┬───────────┘
                             │
                  ┌──────────┴──────────┐
                  │                     │
           [Export Excel]      [Save as Template]
                  │                     │
                  ▼                     ▼
         ┌────────────────┐   ┌────────────────────┐
         │ Download File  │   │ Template Dialog    │
         │ with all data  │   │ • Name template    │
         └────────┬───────┘   │ • Set parameters   │
                  │           │ • Share settings   │
                  │           └────────┬───────────┘
                  │                    │
                  │                    ▼
                  │           ┌────────────────────┐
                  │           │ Template Saved     │
                  │           │ • Appears in sidebar│
                  │           │ • Team can reuse   │
                  │           └────────────────────┘
                  │                    │
                  └────────────────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │   Task Complete      │
                 │   • Accurate data    │
                 │   • Reusable query   │
                 │   • Ready for report │
                 └──────────────────────┘
```

---

## **Scenario 3: Error Recovery and Learning**

### **User Persona**: Dr. Johnson - Quality Improvement Physician

**Context**: Dr. Johnson wants to query patient satisfaction scores but doesn't know the exact terminology used in the database.

**User Goals**:
- Find patient satisfaction data
- Learn from errors
- Get helpful suggestions
- Eventually obtain correct data

**Preconditions**:
- First-time or occasional user
- Limited database knowledge
- Uses clinical terminology (not database terms)

---

### **Primary Flow: Error Discovery and Resolution**

**Step 1: Initial Query with Wrong Terminology**
- **User Action**: Dr. Johnson types:
  ```
  "Show me HCAHPS scores by unit for last month"
  ```
- **System Response**: Submits query, begins processing

**Step 2: Schema Search Failure**
- **System Processing**:
  - RAG searches for "HCAHPS" in schema
  - No exact matches found
  - Searches for similar terms
  - Finds: "patient_satisfaction", "survey_scores", "quality_metrics"
  - Confidence: 0.55 (below threshold)

**Step 3: Helpful Error Message**
- **System Response**:
  - Shows error dialog:
    ```
    ┌─────────────────────────────────────────────────────┐
    │  ℹ️  Data Not Found                                 │
    │                                                     │
    │  I couldn't find "HCAHPS" data in the database.    │
    │                                                     │
    │  Did you mean one of these?                         │
    │  • Patient Satisfaction Scores (survey_scores)      │
    │  • Quality Metrics (quality_metrics)                │
    │  • Patient Experience Data (patient_experience)     │
    │                                                     │
    │  Or would you like to:                              │
    │  • [Browse Available Metrics]                       │
    │  • [Search Database Schema]                         │
    │  • [Rephrase Question]                              │
    │                                                     │
    │  Learn more: HCAHPS is often stored under           │
    │  "Patient Satisfaction" in our database.            │
    └─────────────────────────────────────────────────────┘
    ```

**Step 4: User Selection**
- **User Action**: Clicks "Patient Satisfaction Scores"
- **System Response**:
  - Auto-populates input with corrected query:
    ```
    "Show me patient satisfaction scores by unit for last month"
    ```
  - User can edit or submit directly

**Step 5: Resubmit with Correction**
- **User Action**: Clicks [Submit] or presses Enter
- **System Response**: Processes with correct terminology

**Step 6: Successful Execution**
- **System Processing**:
  - RAG finds `survey_scores` table
  - Finds `unit_name` column
  - Generates correct SQL
  - Executes successfully

**Step 7: Results with Educational Context**
- **System Response**:
  - Shows results table
  - Includes helpful note:
    ```
    ℹ️  Tip: In this database, HCAHPS scores are stored in the 
    'patient_satisfaction_scores' table. I've saved this 
    for future queries.
    ```
  - System updates user's personal context store with:
    - "HCAHPS" → "patient_satisfaction_scores" mapping

**Step 8: Learning Persisted**
- **System Processing**:
  - Next time user mentions "HCAHPS", system automatically maps it
  - No error shown on subsequent similar queries
  - User has learned correct terminology

**Outcome**: User successfully navigates terminology mismatch, learns database structure, and completes task

---

### **Flow Diagram: Error Recovery**

```
┌─────────────────────────────────────┐
│  User Types Query with              │
│  Unknown Term: "HCAHPS"             │
└──────────────┬──────────────────────┘
               │
               ▼
      ┌────────────────┐
      │  Submit Query  │
      └────────┬───────┘
               │
               ▼
      ┌────────────────────┐
      │  RAG Search        │
      │  • Search for      │
      │    "HCAHPS"        │
      │  • Not found!      │
      │  • Low confidence  │
      └────────┬───────────┘
               │
               ▼
      ┌────────────────────┐
      │  Find Similar      │
      │  Terms             │
      │  • "satisfaction"  │
      │  • "survey"        │
      │  • "quality"       │
      └────────┬───────────┘
               │
               ▼
      ┌────────────────────┐
      │  Show Helpful      │
      │  Error Dialog      │
      │  "Did you mean..." │
      │  [Suggestions]     │
      └────────┬───────────┘
               │
    ┌──────────┴───────────┐
    │                      │
    ▼                      ▼
[Select       [Browse    [Rephrase]
Suggestion]   Schema]
    │              │           │
    │              │           └─────────┐
    │              ▼                     │
    │    ┌──────────────────┐            │
    │    │ Schema Browser   │            │
    │    │ Opens, shows     │            │
    │    │ available tables │            │
    │    │ • survey_scores  │            │
    │    │ • quality_metrics│            │
    │    └────────┬─────────┘            │
    │             │                      │
    │             └──────────┬───────────┘
    │                        │
    ▼                        ▼
┌────────────────┐   ┌─────────────────┐
│ Auto-fill Input│   │ User Types New  │
│ with Corrected │   │ Query Manually  │
│ Query          │   │                 │
└────────┬───────┘   └────────┬────────┘
         │                    │
         └────────┬───────────┘
                  │
                  ▼
         ┌────────────────┐
         │ Resubmit Query │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Process with   │
         │ Correct Term   │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Execute SQL    │
         │ Successfully   │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────────────┐
         │ Display Results        │
         │ + Educational Tip      │
         │ "HCAHPS is stored as..."│
         └────────┬───────────────┘
                  │
                  ▼
         ┌────────────────────────┐
         │ Save Mapping           │
         │ "HCAHPS" →             │
         │ "patient_satisfaction" │
         │ to user context        │
         └────────┬───────────────┘
                  │
                  ▼
         ┌────────────────────────┐
         │ Future Queries with    │
         │ "HCAHPS" Work          │
         │ Automatically          │
         └────────────────────────┘
```

---

## **Scenario 4: First-Time User Onboarding**

### **User Persona**: New Hire - Hospital Administrator

**Context**: New employee first day, needs to learn the system quickly to prepare for afternoon meeting.

**User Goals**:
- Understand what the system can do
- Learn how to ask questions
- Build confidence with simple queries
- Get productive within 15 minutes

**Preconditions**:
- Never used the system before
- Has domain knowledge (healthcare) but no SQL
- Completed SSO authentication

---

### **Primary Flow: Guided Onboarding**

**Step 1: First Login**
- **User Action**: Opens application URL after receiving invitation email
- **System Response**:
  - SSO authentication completes
  - Detects first-time user (no query history)
  - Shows welcome modal:
    ```
    ┌─────────────────────────────────────────────────────┐
    │  👋 Welcome to SQL Query Assistant!                 │
    │                                                     │
    │  Ask questions about your data in plain English.   │
    │  I'll translate to SQL and get you answers.        │
    │                                                     │
    │  What would you like to do?                         │
    │  • [Take 2-Minute Tour] (Recommended)               │
    │  • [See Example Queries]                            │
    │  • [Start Querying Now]                             │
    │                                                     │
    │  Don't show this again [checkbox]                   │
    └─────────────────────────────────────────────────────┘
    ```

**Step 2: Interactive Tutorial**
- **User Action**: Clicks [Take 2-Minute Tour]
- **System Response**:
  - Starts guided tour with spotlight highlighting
  - **Tour Step 1**: Query Input
    ```
    ┌─────────────────────────────────────┐
    │  Type your question here in        │
    │  natural language.                 │
    │                                    │
    │  Try: "How many patients were      │
    │  admitted yesterday?"              │
    │                                    │
    │  [Next]                            │
    └─────────────────────────────────────┘
    ```

**Step 3: Tutorial Continues**
- **Tour Step 2**: Example Queries
  - Highlights example query dropdown
  - "Click here for pre-written examples"
  
- **Tour Step 3**: History Sidebar
  - Highlights history panel
  - "Your past queries appear here for quick access"
  
- **Tour Step 4**: Schema Browser
  - Highlights schema browser
  - "Explore available data tables"
  
- **Tour Step 5**: Results Area
  - Shows what results look like
  - "You'll see both SQL and results here"

**Step 4: Try First Query**
- **System Response**:
  - Tour ends with prompt:
    ```
    ┌─────────────────────────────────────┐
    │  Ready to try your first query?    │
    │                                    │
    │  I'll suggest an easy one:         │
    │  "How many patients were admitted  │
    │  last week?"                       │
    │                                    │
    │  [Try This Query] [Choose My Own]  │
    └─────────────────────────────────────┘
    ```

**Step 5: First Query Execution**
- **User Action**: Clicks [Try This Query]
- **System Response**:
  - Auto-fills input with suggested query
  - Highlights Submit button
  - User clicks Submit
  - Query processes normally

**Step 6: First Success Experience**
- **System Response**:
  - Shows results with celebration animation ✨
  - Overlay message:
    ```
    ┌─────────────────────────────────────┐
    │  🎉 Great Job!                      │
    │                                    │
    │  You just ran your first query.    │
    │  The system:                       │
    │  1. Understood your question       │
    │  2. Found the right data tables    │
    │  3. Generated SQL                  │
    │  4. Got your answer: 147 patients  │
    │                                    │
    │  [Try Another] [Explore Examples]  │
    └─────────────────────────────────────┘
    ```

**Step 7: Build Confidence**
- **User Action**: Clicks [Explore Examples]
- **System Response**:
  - Opens example library with categories
  - User selects "Daily Operations" category
  - Sees 10 common operational queries
  - Clicks example: "Today's census by unit"

**Step 8: Second Query**
- **System Response**:
  - Executes example query
  - Shows results
  - User realizes the pattern
  - Tries modifying query: "Yesterday's census by unit"
  - System handles modification correctly

**Step 9: Onboarding Complete**
- **System Response**:
  - After 3 successful queries, shows completion badge:
    ```
    ┌─────────────────────────────────────┐
    │  ⭐ You're Ready!                   │
    │                                    │
    │  You've successfully:              │
    │  ✓ Completed the tutorial          │
    │  ✓ Run 3 queries                   │
    │  ✓ Explored examples               │
    │                                    │
    │  Resources:                        │
    │  • User Manual                     │
    │  • Video Tutorials                 │
    │  • Support (Help icon)             │
    │                                    │
    │  [Start Working]                   │
    └─────────────────────────────────────┘
    ```

**Outcome**: User is productive within 10 minutes, confident to use system independently

---

## **Scenario 5: Query Refinement Through Conversation**

### **User Persona**: Sarah - Operations Manager (Returning User)

**Context**: Sarah needs to drill down from high-level metrics to specific details through iterative queries.

**User Goals**:
- Start broad, then narrow focus
- Maintain context across multiple queries
- Quickly pivot analysis direction
- No need to repeat information

---

### **Conversation Flow**

**Query 1: Initial Broad Query**
```
User: "Show me today's admissions"

System: 
  ✓ 87 patients admitted today
  
  [Table: Simple count]
  
  Conversation context stored: today's admissions
```

**Query 2: Follow-up with Grouping**
```
User: "Break it down by patient type"

System (understands "it" = today's admissions):
  ✓ Today's admissions by patient type
  
  [Table]
  Patient Type | Count
  Inpatient    | 45
  Outpatient   | 28
  Emergency    | 14
  
  Conversation context: today's admissions, by patient type
```

**Query 3: Further Drilling Down**
```
User: "Show me the emergency patients"

System (knows "emergency patients" = subset from previous):
  ✓ 14 emergency admissions today
  
  [Table with patient details]
  MRN | Age | Arrival Time | Chief Complaint | ...
  
  Conversation context: today's emergency admissions
```

**Query 4: Pivot to Different Dimension**
```
User: "Go back to all admissions. Show me by hour instead."

System (recognizes "go back" instruction):
  ✓ Today's admissions by hour
  
  [Table]
  Hour  | Admissions
  00:00 | 2
  01:00 | 1
  ...
  08:00 | 12
  
  Conversation context reset to: today's admissions, by hour
```

**Query 5: Comparison Query**
```
User: "How does this compare to yesterday?"

System (compares same metric for previous day):
  ✓ Admission comparison: Today vs Yesterday
  
  [Table]
  Hour  | Today | Yesterday | Difference
  00:00 | 2     | 3         | -1
  ...
  
  Conversation context: today vs yesterday admissions by hour
```

---

### **Flow Diagram: Conversation Refinement**

```
┌──────────────────────────────────────────────┐
│  Query 1: "Show me today's admissions"      │
└────────────────────┬─────────────────────────┘
                     │
                     ▼
          ┌──────────────────┐
          │  Execute Query   │
          │  Result: 87      │
          │  Save Context    │
          └────────┬─────────┘
                   │
                   │  Conversation Memory:
                   │  • Subject: admissions
                   │  • Date: today
                   │  • Last SQL: SELECT COUNT(*)...
                   │
                   ▼
┌──────────────────────────────────────────────┐
│  Query 2: "Break it down by patient type"   │
│  (System resolves "it" = previous subject)  │
└────────────────────┬─────────────────────────┘
                     │
                     ▼
          ┌──────────────────┐
          │  Modify Last SQL │
          │  Add GROUP BY    │
          │  patient_type    │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │  Results Table   │
          │  3 patient types │
          │  Update Context  │
          └────────┬─────────┘
                   │
                   │  Memory Updated:
                   │  • + Grouping: patient_type
                   │
                   ▼
┌──────────────────────────────────────────────┐
│  Query 3: "Show me the emergency patients"  │
│  (Adds filter to current context)           │
└────────────────────┬─────────────────────────┘
                     │
                     ▼
          ┌──────────────────┐
          │  Add WHERE       │
          │  patient_type =  │
          │  'Emergency'     │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │  Detail View     │
          │  14 rows         │
          └────────┬─────────┘
                   │
                   │  Memory: Now filtered to
                   │  emergency only
                   │
                   ▼
┌──────────────────────────────────────────────┐
│  Query 4: "Go back to all admissions.       │
│  Show me by hour instead."                  │
│  (Explicit context reset + new grouping)    │
└────────────────────┬─────────────────────────┘
                     │
                     ▼
          ┌──────────────────┐
          │  Reset Filter    │
          │  Change GROUP BY │
          │  to hour         │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │  Hourly Breakdown│
          │  24 rows         │
          └────────┬─────────┘
                   │
                   │  Memory: Back to all
                   │  admissions, by hour
                   │
                   ▼
┌──────────────────────────────────────────────┐
│  Query 5: "How does this compare to         │
│  yesterday?"                                │
│  (Adds temporal comparison)                 │
└────────────────────┬─────────────────────────┘
                     │
                     ▼
          ┌──────────────────┐
          │  Replicate Query │
          │  for Yesterday   │
          │  UNION results   │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │  Comparison Table│
          │  Today vs Yest.  │
          └──────────────────┘
```

**Key Decision Points in Conversation Management:**

1. **Pronoun Resolution**: "it", "them", "these" → previous query subject
2. **Context Continuation**: "also show...", "add..." → modify existing query
3. **Context Reset**: "go back", "start over", "now show me..." → new query
4. **Context Narrowing**: "just the...", "only..." → add filters
5. **Context Expansion**: "include...", "add..." → remove filters/add columns
6. **Temporal Shifts**: "yesterday", "last week" → change date parameters

---

## **Scenario 6: Data Export and Sharing**

### **User Persona**: Mark - Data Analyst

**Context**: Mark needs to share query results with stakeholders who don't have system access.

**User Goals**:
- Export results in multiple formats
- Include context (SQL, metadata) for transparency
- Schedule recurring reports
- Share securely

---

### **Export Flow**

**Step 1: After Successful Query**
- **System State**: Results displayed (347 rows)
- **Available Options**:
  - [Export to CSV]
  - [Export to Excel]
  - [Copy to Clipboard]
  - [Schedule Report]
  - [Share Link]

**Step 2: Excel Export**
- **User Action**: Clicks [Export to Excel]
- **System Response**:
  - Shows export options dialog:
    ```
    ┌─────────────────────────────────────┐
    │  Export to Excel                   │
    │                                    │
    │  Include in export:                │
    │  ☑ Query results (347 rows)        │
    │  ☑ SQL query                       │
    │  ☑ Metadata (timestamp, user)      │
    │  ☐ Data dictionary                 │
    │                                    │
    │  Format options:                   │
    │  ☑ Format numbers                  │
    │  ☑ Auto-fit columns                │
    │  ☑ Freeze header row               │
    │                                    │
    │  [Export]  [Cancel]                │
    └─────────────────────────────────────┘
    ```

**Step 3: File Generation**
- **System Processing**:
  - Generates XLSX file with multiple sheets:
    - Sheet 1: "Results" - formatted data table
    - Sheet 2: "Query Details" - SQL, execution time, filters
    - Sheet 3: "Data Dictionary" (if selected) - column definitions
  - Adds metadata in header:
    - Query date/time
    - Generated by: Mark Johnson
    - Database: Production
  - File name: `readmission_analysis_2025-10-29_0843.xlsx`

**Step 4: Download Complete**
- **System Response**:
  - Browser downloads file
  - Success notification: "Report exported successfully"
  - Option to [Open File] or [Export Another Format]

**Step 5: Schedule Recurring Report**
- **User Action**: Clicks [Schedule Report]
- **System Response**:
  - Opens scheduling dialog:
    ```
    ┌─────────────────────────────────────┐
    │  Schedule Recurring Report         │
    │                                    │
    │  Query: "30-day readmission rate   │
    │  by service line"                  │
    │                                    │
    │  Frequency:                        │
    │  ○ Daily                           │
    │  ○ Weekly (Monday)                 │
    │  ● Monthly (1st of month)          │
    │  ○ Quarterly                       │
    │                                    │
    │  Time: [08:00 AM] [EST ▼]         │
    │                                    │
    │  Delivery:                         │
    │  ☑ Email to: mark.johnson@...     │
    │  ☑ Save to shared folder           │
    │  ☐ Post to Teams channel           │
    │                                    │
    │  Dynamic date range:               │
    │  ● Previous month                  │
    │  ○ Last 30 days                    │
    │  ○ Custom                          │
    │                                    │
    │  [Schedule]  [Cancel]              │
    └─────────────────────────────────────┘
    ```

**Step 6: Scheduled Report Confirmation**
- **User Action**: Configures options, clicks [Schedule]
- **System Response**:
  - Creates scheduled job
  - Confirmation message:
    ```
    ✓ Report scheduled successfully
    
    Next run: November 1, 2025 at 8:00 AM EST
    
    View all scheduled reports in [My Reports]
    ```

**Outcome**: Data exported for offline analysis and automated for recurring needs

---

## **Scenario 7: Schema Exploration and Discovery**

### **User Persona**: New Analyst - First Week on Job

**Context**: Analyst needs to understand available data before querying.

**User Goals**:
- Discover what data exists
- Understand table relationships
- Find relevant metrics
- Learn business terminology

---

### **Schema Exploration Flow**

**Step 1: Access Schema Browser**
- **User Action**: Clicks "Schema Browser" tab in sidebar
- **System Response**:
  - Opens tree view of database structure
  - Shows databases → schemas → tables hierarchy
  - Search bar at top

**Step 2: Browse Tables**
- **User Action**: Expands "Production" database
- **System Response**:
  - Shows schemas:
    - dbo (125 tables)
    - reporting (43 tables)
    - staging (18 tables)
  - User expands "dbo" schema

**Step 3: Explore Table Details**
- **User Action**: Clicks on `pt_accounting_reporting_alt` table
- **System Response**:
  - Opens table detail panel:
    ```
    ┌─────────────────────────────────────────────┐
    │  pt_accounting_reporting_alt                │
    │  Patient Accounting and Reporting           │
    │  ─────────────────────────────────────────  │
    │                                             │
    │  Description:                               │
    │  Contains patient encounter financial and   │
    │  administrative data including admissions,  │
    │  discharges, and account details.           │
    │                                             │
    │  Row Count: ~2.5M records                   │
    │  Last Updated: 2025-10-29 00:15             │
    │                                             │
    │  Columns (18):                              │
    │  ┌──────────────┬──────────┬─────────────┐ │
    │  │ Column       │ Type     │ Description │ │
    │  ├──────────────┼──────────┼─────────────┤ │
    │  │ encounter_id │ INT      │ Unique ID   │ │
    │  │ patient_id   │ INT      │ Patient ref │ │
    │  │ acct_type    │ VARCHAR  │ IP/OP/ED    │ │
    │  │ admit_date   │ DATE     │ Admission   │ │
    │  │ dsch_date    │ DATE     │ Discharge   │ │
    │  │ dsch_disp    │ VARCHAR  │ Disposition │ │
    │  │ ...          │ ...      │ ...         │ │
    │  └──────────────┴──────────┴─────────────┘ │
    │                                             │
    │  Sample Values:                             │
    │  acct_type: 'IP' (45%), 'OP' (38%), ...    │
    │  dsch_disp: 'Home' (62%), 'SNF' (22%), ... │
    │                                             │
    │  Relationships:                             │
    │  • → patient_master (patient_id)            │
    │  • → service_line_master (service_line_id)  │
    │                                             │
    │  Common Queries Using This Table:           │
    │  • Daily discharge counts                   │
    │  • Length of stay calculations              │
    │  • Census reports                           │
    │                                             │
    │  [Query This Table]  [See Example Queries]  │
    └─────────────────────────────────────────────┘
    ```

**Step 4: Launch Query from Schema**
- **User Action**: Clicks [Query This Table]
- **System Response**:
  - Switches to query interface
  - Auto-populates input with table context:
    ```
    "Show me data from pt_accounting_reporting_alt table"
    ```
  - Provides suggestions:
    - "Show me records from the last 7 days"
    - "Count records by account type"
    - "Show average length of stay"

**Step 5: Contextual Query**
- **User Action**: Modifies to: "Show me admissions from last week"
- **System Response**:
  - Uses schema context from browser
  - Knows table structure already
  - Generates accurate SQL quickly

**Outcome**: User understands data structure before querying, leading to better questions

---

## **Scenario 8: System Administrator - Configuration and Monitoring**

### **User Persona**: IT Administrator

**Context**: Admin needs to monitor system health, manage users, and update configurations.

**User Goals**:
- Monitor system performance
- Manage user access
- Update schema when database changes
- Troubleshoot issues

---

### **Admin Flow**

**Step 1: Access Admin Panel**
- **User Action**: Clicks user menu → [Administration]
- **System Response**:
  - Verifies admin role
  - Opens admin dashboard
  - Shows tabs:
    - System Health
    - User Management
    - Schema Management
    - Query Logs
    - Settings

**Step 2: Monitor System Health**
- **System State**: Dashboard displays:
  ```
  ┌─────────────────────────────────────────┐
  │  System Health Overview                 │
  │  Status: ✓ All systems operational      │
  │  ─────────────────────────────────────  │
  │                                         │
  │  LLM Service:        ✓ Online          │
  │  • Model: SQLCoder-7B                   │
  │  • Avg response: 2.3s                   │
  │  • Requests/min: 12                     │
  │                                         │
  │  Database:           ✓ Connected        │
  │  • Connection pool: 7/20 active         │
  │  • Avg query time: 1.1s                 │
  │  • Failed queries: 3 (last hour)        │
  │                                         │
  │  Vector Store:       ✓ Online          │
  │  • Documents: 8,432                     │
  │  • Avg retrieval: 0.4s                  │
  │  • Last indexed: 6 hours ago            │
  │                                         │
  │  Application:        ✓ Running          │
  │  • Active users: 14                     │
  │  • Uptime: 23 days, 14 hours            │
  │  • Memory usage: 6.2GB / 16GB           │
  │  • CPU usage: 34%                       │
  │                                         │
  │  [View Detailed Metrics]  [Alerts (0)]  │
  └─────────────────────────────────────────┘
  ```

**Step 3: Schema Refresh Trigger**
- **User Action**: Clicks Schema Management tab
- **System Response**: Shows schema status:
  ```
  ┌─────────────────────────────────────────┐
  │  Schema Management                      │
  │  ─────────────────────────────────────  │
  │                                         │
  │  Current Schema Version: 2025.10.29     │
  │  Last Refresh: 6 hours ago              │
  │  Next Scheduled: Today at 12:00 AM      │
  │                                         │
  │  Schema Statistics:                     │
  │  • Tables: 186                          │
  │  • Columns: 3,247                       │
  │  • Relationships: 412                   │
  │  • Indexed documents: 8,432             │
  │                                         │
  │  Recent Changes:                        │
  │  • Oct 28: Added patient_survey table   │
  │  • Oct 25: Modified encounters schema   │
  │  • Oct 20: Dropped temp_imports table   │
  │                                         │
  │  [Refresh Now]  [View Change History]   │
  │  [Configure Auto-Refresh]               │
  └─────────────────────────────────────────┘
  ```

**Step 4: Manual Schema Refresh**
- **User Action**: Clicks [Refresh Now]
- **System Response**:
  - Starts schema extraction process
  - Progress indicator:
    ```
    Refreshing database schema...
    
    ✓ Connecting to database
    ✓ Extracting table metadata (186 tables)
    ⏳ Generating embeddings... 52%
    ⏳ Updating vector store...
    ⏳ Detecting changes...
    ```
  - Completes in 3 minutes
  - Shows summary:
    ```
    Schema refresh complete!
    
    Changes detected:
    • 2 new tables added
    • 7 columns modified
    • 1 table dropped
    
    [View Details]  [Notify Users of Changes]
    ```

**Step 5: User Management**
- **User Action**: Clicks User Management tab
- **System Response**: Shows user list with actions:
  ```
  ┌─────────────────────────────────────────────────────┐
  │  User Management                        [Add User]  │
  │  ─────────────────────────────────────────────────  │
  │                                                     │
  │  Active Users: 45                                   │
  │                                                     │
  │  [Search users...] [Filter by Role ▼] [Export]     │
  │                                                     │
  │  Name              Role      Last Active  Queries   │
  │  Sarah Mitchell    Viewer    5 min ago    1,247    │
  │  Mark Johnson      Analyst   Active now   3,891    │
  │  Dr. Lisa Chen     Viewer    2 hours ago  423      │
  │  ...                                                │
  │                                                     │
  │  [Edit]  [Deactivate]  [View Activity]             │
  └─────────────────────────────────────────────────────┘
  ```

**Outcome**: Admin maintains healthy system, proactively manages issues

---

## **Decision Point Matrix: System Behavior**

### **Key Decision Points Across Scenarios**

| **Situation** | **Trigger** | **Decision** | **Action** |
|---------------|-------------|--------------|------------|
| **Ambiguous Query** | Confidence < 0.7 | Ask clarification | Show options dialog |
| **SQL Validation Failure** | Table not found | Auto-retry | Regenerate with error context |
| **Complex Query** | 4+ table JOINs | Warn user | Show preview, allow review |
| **Timeout** | Query > 30s | Cancel | Show timeout error with suggestions |
| **First Login** | No query history | Onboard | Show welcome tutorial |
| **Follow-up Query** | Pronoun detected | Use context | Reference previous query |
| **Unknown Term** | Schema match < 0.5 | Suggest alternatives | Show "Did you mean..." |
| **Large Result Set** | > 1000 rows | Paginate | Show 100 rows per page |
| **Schema Change** | New table detected | Notify admin | Send alert, update vectors |

---

## **Summary: User Scenario Coverage**

**Total Scenarios**: 8 comprehensive scenarios covering:

1. ✅ **Simple Daily Operations** - Most common use case (80% of queries)
2. ✅ **Complex Analytics** - Advanced users, multi-table queries
3. ✅ **Error Recovery** - Learning from mistakes, helpful guidance
4. ✅ **First-Time User** - Onboarding, building confidence
5. ✅ **Conversational Refinement** - Follow-up queries, context maintenance
6. ✅ **Data Export** - Sharing results, scheduling reports
7. ✅ **Schema Exploration** - Discovery, learning database structure
8. ✅ **Administration** - System management, monitoring

**Flow Characteristics**:
- **Happy paths**: Successful task completion
- **Alternative paths**: Error handling, different user choices
- **Decision points**: System logic branches
- **Error recovery**: Graceful failure handling
- **Progressive disclosure**: Simple → advanced features

Each scenario includes:
- User context and goals
- Step-by-step interactions
- System responses
- Visual flow diagrams
- Decision points
- Success criteria
- Alternative outcomes

These scenarios drive:
- Feature prioritization
- UI/UX design decisions
- Testing strategies
- Documentation structure
- Training materials
- Support procedures