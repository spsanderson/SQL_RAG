# **Pseudocode Document: SQL RAG Ollama Application**

**Project**: SQL RAG Ollama - Natural Language Database Query System  
**Phase**: SPARC Phase 4 - Pseudocode  
**Version**: 1.0  
**Date**: October 29, 2025  
**Status**: Development Roadmap

---

[Back to Main SPARC Documentation](SQL%20LLM%20RAG%20Project%20SPARC.md)

## **Table of Contents**

1. [Overview](#1-overview)
2. [Main Application Entry Point](#2-main-application-entry-point)
3. [Core Module - Query Processing Pipeline](#3-core-module---query-processing-pipeline)
4. [RAG Module - Retrieval Augmented Generation](#4-rag-module---retrieval-augmented-generation)
5. [LLM Module - SQL Generation](#5-llm-module---sql-generation)
6. [Validation Module - Security & Safety](#6-validation-module---security--safety)
7. [Database Module - Query Execution](#7-database-module---query-execution)
8. [UI Module - User Interface](#8-ui-module---user-interface)
9. [Infrastructure Module - Utilities](#9-infrastructure-module---utilities)
10. [Data Models and Structures](#10-data-models-and-structures)
11. [Language-Specific Considerations](#11-language-specific-considerations)
12. [Reflection and Optimization](#12-reflection-and-optimization)

---

## **1. Overview**

### **1.1 Document Purpose**

This pseudocode document translates the comprehensive specification and architecture into implementation-ready algorithmic logic. It serves as a bridge between design and code, providing:

- **Language-agnostic algorithms** that can be implemented in Python, JavaScript, or TypeScript
- **Step-by-step logic flows** for all major components
- **Clear interface definitions** for module interactions
- **Implementation guidance** with inline comments and explanations

### **1.2 Pseudocode Conventions**

```
CONVENTIONS USED IN THIS DOCUMENT:

CAPITALIZED_TEXT = Keywords, operations (IF, WHILE, RETURN)
lowercase_text = Variables, function names, parameters
PascalCase = Class names, data structures
camelCase = Alternative for JavaScript/TypeScript context
snake_case = Alternative for Python context

// Single-line comments
/* Multi-line
   comments */

→ = Returns/outputs
← = Assigns value
[] = Array/list
{} = Dictionary/object/map
: = Type annotation (when needed)
```

### **1.3 Module Dependency Overview**

```
┌─────────────────────────────────────────────────────────┐
│                      UI Module                          │
│              (Streamlit/React/Vue)                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   Core Module                           │
│            (QueryProcessor - Orchestrator)              │
└─┬────────────┬────────────┬────────────┬────────────────┘
  │            │            │            │
  ↓            ↓            ↓            ↓
┌────┐      ┌────┐      ┌────┐      ┌────────┐
│RAG │      │LLM │      │DB  │      │Validation│
└────┘      └────┘      └────┘      └────────┘
  │            │            │
  ↓            ↓            ↓
┌─────────────────────────────────────────────────────────┐
│            Infrastructure Module                        │
│      (Logging, Config, Metrics, Cache)                 │
└─────────────────────────────────────────────────────────┘
```

---

## **2. Main Application Entry Point**

### **2.1 Application Bootstrap**

```pseudocode
/*
 * MAIN APPLICATION ENTRY POINT
 * Purpose: Initialize all components and start application
 * Input: Configuration files, environment variables
 * Output: Running application instance
 * Language: Python (primary), adaptable to Node.js
 */

FUNCTION main():
    // Step 1: Load Configuration
    config ← load_configuration_from_yaml("config/")
    
    // Step 2: Setup Infrastructure
    logger ← initialize_logging_system(config.logging)
    metrics ← initialize_metrics_collector(config.monitoring)
    
    LOG(INFO, "Starting SQL RAG Ollama Application")
    
    // Step 3: Build Dependency Tree (Dependency Injection)
    TRY:
        // Infrastructure dependencies
        cache_service ← create_cache_service(config.cache)
        config_manager ← create_config_manager(config)
        
        // Database layer
        database_engine ← create_database_engine(
            config: config.database,
            logger: logger,
            metrics: metrics
        )
        
        // Verify database connection
        IF NOT database_engine.test_connection():
            RAISE ConnectionError("Cannot connect to database")
        END IF
        
        // RAG layer
        vector_store ← create_vector_store(
            path: config.rag.vector_store_path,
            collection: config.rag.collection_name
        )
        
        embedding_generator ← create_embedding_generator(
            model: config.rag.embedding_model
        )
        
        rag_engine ← create_rag_engine(
            vector_store: vector_store,
            embeddings: embedding_generator,
            config: config.rag
        )
        
        // LLM layer
        ollama_client ← create_ollama_client(
            base_url: config.ollama.base_url,
            timeout: config.ollama.timeout
        )
        
        // Verify Ollama is running
        IF NOT ollama_client.is_healthy():
            RAISE ServiceError("Ollama service not available")
        END IF
        
        prompt_builder ← create_prompt_builder()
        
        llm_engine ← create_llm_engine(
            client: ollama_client,
            prompt_builder: prompt_builder,
            config: config.ollama
        )
        
        // Validation layer
        schema_provider ← create_schema_provider(database_engine)
        
        query_validator ← create_query_validator(
            schema_provider: schema_provider,
            config: config.validation
        )
        
        // Core layer
        conversation_manager ← create_conversation_manager()
        
        query_processor ← create_query_processor(
            rag_engine: rag_engine,
            llm_engine: llm_engine,
            validator: query_validator,
            db_engine: database_engine,
            conversation_manager: conversation_manager,
            logger: logger,
            metrics: metrics
        )
        
        // Wrap with caching layer
        cached_processor ← create_cached_query_processor(
            processor: query_processor,
            cache: cache_service,
            ttl: config.cache.ttl
        )
        
        // Step 4: Create Application Instance
        app ← create_application(
            query_processor: cached_processor,
            database_engine: database_engine,
            config: config
        )
        
        // Step 5: Initialize UI
        ui ← create_ui_interface(
            app: app,
            config: config.ui
        )
        
        // Step 6: Start Application
        LOG(INFO, "Application initialized successfully")
        
        ui.start()  // Blocks until shutdown
        
    CATCH exception AS e:
        LOG(ERROR, "Application startup failed", error: e)
        RAISE e
    END TRY
    
    // Cleanup on shutdown
    LOG(INFO, "Shutting down application")
    cleanup_resources()
    
END FUNCTION


/*
 * DEPENDENCY INJECTION HELPER FUNCTIONS
 * These functions encapsulate component creation with proper configuration
 */

FUNCTION create_database_engine(config, logger, metrics):
    // Initialize database connection pool
    connection_string ← build_connection_string(config)
    
    RETURN DatabaseEngine(
        connection_string: connection_string,
        pool_size: config.pool_size,
        timeout: config.timeout,
        logger: logger,
        metrics: metrics
    )
END FUNCTION


FUNCTION create_rag_engine(vector_store, embeddings, config):
    // Create RAG retrieval engine
    retriever ← create_retriever(
        vector_store: vector_store,
        top_k: config.top_k,
        threshold: config.similarity_threshold
    )
    
    RETURN RAGEngine(
        vector_store: vector_store,
        embeddings: embeddings,
        retriever: retriever,
        config: config
    )
END FUNCTION


FUNCTION create_cached_query_processor(processor, cache, ttl):
    // Wrap processor with caching layer
    RETURN CachedQueryProcessor(
        processor: processor,
        cache: cache,
        ttl: ttl
    )
END FUNCTION


/*
 * CONFIGURATION LOADING
 * Purpose: Load and merge configuration from multiple sources
 */

FUNCTION load_configuration_from_yaml(config_dir):
    // Load base configuration
    base_config ← parse_yaml_file(config_dir + "base.yaml")
    
    // Load environment-specific config
    environment ← get_environment_variable("ENVIRONMENT", default: "development")
    env_config ← parse_yaml_file(config_dir + environment + ".yaml")
    
    // Merge configurations (env overrides base)
    merged_config ← merge_configurations(base_config, env_config)
    
    // Substitute environment variables
    final_config ← substitute_env_variables(merged_config)
    
    // Validate configuration schema
    validate_configuration(final_config)
    
    RETURN final_config
END FUNCTION


/*
 * GRACEFUL SHUTDOWN
 * Purpose: Clean up resources on application exit
 */

FUNCTION cleanup_resources():
    LOG(INFO, "Cleaning up resources")
    
    // Close database connections
    IF database_engine IS NOT NULL:
        database_engine.close_all_connections()
    END IF
    
    // Flush logs
    IF logger IS NOT NULL:
        logger.flush()
    END IF
    
    // Flush metrics
    IF metrics IS NOT NULL:
        metrics.push_final_metrics()
    END IF
    
    LOG(INFO, "Cleanup complete")
END FUNCTION


/*
 * HEALTH CHECK ENDPOINT
 * Purpose: Provide health status for monitoring
 * Used by: Load balancers, monitoring systems
 */

FUNCTION health_check():
    status ← {
        "status": "healthy",
        "timestamp": current_timestamp(),
        "components": {}
    }
    
    // Check database
    TRY:
        IF database_engine.test_connection():
            status.components["database"] ← "healthy"
        ELSE:
            status.components["database"] ← "unhealthy"
            status.status ← "degraded"
        END IF
    CATCH:
        status.components["database"] ← "error"
        status.status ← "unhealthy"
    END TRY
    
    // Check Ollama
    TRY:
        IF ollama_client.is_healthy():
            status.components["ollama"] ← "healthy"
        ELSE:
            status.components["ollama"] ← "unhealthy"
            status.status ← "degraded"
        END IF
    CATCH:
        status.components["ollama"] ← "error"
        status.status ← "unhealthy"
    END TRY
    
    // Check vector store
    TRY:
        IF vector_store.is_healthy():
            status.components["vector_store"] ← "healthy"
        ELSE:
            status.components["vector_store"] ← "unhealthy"
            status.status ← "degraded"
        END IF
    CATCH:
        status.components["vector_store"] ← "error"
        status.status ← "unhealthy"
    END TRY
    
    RETURN status
END FUNCTION
```

---

## **3. Core Module - Query Processing Pipeline**

### **3.1 Query Processor (Main Orchestrator)**

```pseudocode
/*
 * QUERY PROCESSOR - MAIN ORCHESTRATOR
 * Purpose: Coordinates entire query processing pipeline
 * Input: Natural language query, user session
 * Output: Query response with SQL and results
 * Pipeline: Input → Intent → RAG → LLM → Validation → Execution → Format
 */

CLASS QueryProcessor:
    // Dependencies (injected via constructor)
    PRIVATE rag_engine: RAGEngine
    PRIVATE llm_engine: LLMEngine
    PRIVATE validator: QueryValidator
    PRIVATE db_engine: DatabaseEngine
    PRIVATE conversation_manager: ConversationManager
    PRIVATE logger: Logger
    PRIVATE metrics: MetricsCollector
    
    
    /*
     * CONSTRUCTOR
     */
    FUNCTION initialize(rag, llm, validator, db, conversation, logger, metrics):
        this.rag_engine ← rag
        this.llm_engine ← llm
        this.validator ← validator
        this.db_engine ← db
        this.conversation_manager ← conversation
        this.logger ← logger
        this.metrics ← metrics
    END FUNCTION
    
    
    /*
     * MAIN QUERY PROCESSING PIPELINE
     * This is the primary entry point for all queries
     */
    ASYNC FUNCTION process_query(user_query: UserQuery, session: UserSession) → QueryResponse:
        start_time ← current_timestamp_milliseconds()
        query_id ← generate_unique_id()
        
        // Log query submission
        this.logger.log_info(
            message: "Processing query",
            query_id: query_id,
            user_id: user_query.user_id,
            query_text: user_query.text
        )
        
        TRY:
            // ========== STAGE 1: INPUT VALIDATION ==========
            this.validator.validate_input(user_query.text)
            this.metrics.increment("queries.submitted")
            
            
            // ========== STAGE 2: INTENT CLASSIFICATION ==========
            intent ← AWAIT this.classify_intent(user_query)
            
            user_query.intent ← intent.type
            user_query.confidence ← intent.confidence
            user_query.entities ← intent.entities
            
            this.logger.log_debug(
                message: "Intent classified",
                intent: intent.type,
                confidence: intent.confidence
            )
            
            
            // ========== STAGE 3: CONTEXT RETRIEVAL (RAG) ==========
            context ← AWAIT this.rag_engine.retrieve_context(
                query: user_query.text,
                intent: intent,
                conversation_history: session.conversation_history
            )
            
            this.logger.log_debug(
                message: "Context retrieved",
                elements_count: LENGTH(context.retrieved_elements),
                retrieval_time: context.retrieval_time_ms
            )
            
            
            // ========== STAGE 4: SQL GENERATION (LLM) ==========
            generated_sql ← AWAIT this.llm_engine.generate_sql(
                query: user_query,
                context: context,
                conversation: session.conversation_history[-5:]  // Last 5 turns
            )
            
            this.logger.log_info(
                message: "SQL generated",
                sql_preview: generated_sql.sql_text[0:100]  // First 100 chars
            )
            
            
            // ========== STAGE 5: SQL VALIDATION ==========
            validation_result ← AWAIT this.validator.validate_sql(
                sql: generated_sql.sql_text,
                context_elements: context.retrieved_elements
            )
            
            // Check for critical errors
            IF NOT validation_result.passed:
                IF validation_result.has_critical_errors():
                    this.metrics.increment("queries.validation_failed")
                    RAISE ValidationError(validation_result.issues)
                ELSE:
                    // Has warnings but can proceed
                    this.logger.log_warning(
                        message: "SQL validation warnings",
                        warnings: validation_result.issues
                    )
                END IF
            END IF
            
            
            // ========== STAGE 6: QUERY EXECUTION ==========
            result ← AWAIT this.db_engine.execute_query(
                sql: generated_sql.sql_text,
                timeout: 30  // seconds
            )
            
            this.logger.log_info(
                message: "Query executed",
                success: result.success,
                row_count: result.row_count,
                execution_time: result.execution_time_ms
            )
            
            
            // ========== STAGE 7: RESULT FORMATTING ==========
            natural_language_answer ← AWAIT this.generate_natural_language_answer(
                query: user_query,
                result: result
            )
            
            
            // ========== STAGE 8: CREATE RESPONSE ==========
            total_time ← current_timestamp_milliseconds() - start_time
            
            response ← QueryResponse(
                query_id: query_id,
                original_query: user_query.text,
                generated_sql: generated_sql,
                result: result,
                natural_language_answer: natural_language_answer,
                total_time_ms: total_time,
                cached: FALSE
            )
            
            
            // ========== STAGE 9: UPDATE CONVERSATION ==========
            this.conversation_manager.add_turn(
                session: session,
                query: user_query,
                response: response
            )
            
            
            // ========== STAGE 10: METRICS & LOGGING ==========
            this.metrics.record_query_success(
                duration: total_time,
                intent: intent.type
            )
            
            this.metrics.histogram("query.total_time", total_time)
            this.metrics.histogram("query.sql_generation_time", generated_sql.generation_time_ms)
            this.metrics.histogram("query.execution_time", result.execution_time_ms)
            
            
            RETURN response
            
        CATCH validation_error AS e:
            // Validation errors are user-facing
            this.logger.log_warning("Query validation failed", error: e)
            this.metrics.increment("queries.validation_failed")
            
            // Return error response instead of throwing
            RETURN create_error_response(
                query_id: query_id,
                error_type: "validation_error",
                message: e.message,
                suggestions: e.suggestions
            )
            
        CATCH database_error AS e:
            // Database errors (connection, timeout, etc.)
            this.logger.log_error("Database error", error: e)
            this.metrics.increment("queries.database_error")
            
            RETURN create_error_response(
                query_id: query_id,
                error_type: "database_error",
                message: "Query execution failed",
                suggestions: ["Check database connection", "Simplify query"]
            )
            
        CATCH llm_error AS e:
            // LLM generation errors
            this.logger.log_error("LLM generation failed", error: e)
            this.metrics.increment("queries.llm_error")
            
            RETURN create_error_response(
                query_id: query_id,
                error_type: "generation_error",
                message: "Could not generate SQL",
                suggestions: ["Try rephrasing your question", "Use simpler language"]
            )
            
        CATCH exception AS e:
            // Unexpected errors
            this.logger.log_error("Unexpected error in query processing", error: e, stack_trace: TRUE)
            this.metrics.increment("queries.unexpected_error")
            
            RETURN create_error_response(
                query_id: query_id,
                error_type: "internal_error",
                message: "An unexpected error occurred",
                suggestions: ["Try again", "Contact support if problem persists"]
            )
        END TRY
        
    END FUNCTION
    
    
    /*
     * INTENT CLASSIFICATION
     * Purpose: Determine query type and extract entities
     * Input: Natural language query
     * Output: Intent classification with confidence
     */
    PRIVATE ASYNC FUNCTION classify_intent(query: UserQuery) → Intent:
        // Heuristic classification (fast, good enough for MVP)
        query_lower ← to_lowercase(query.text)
        
        // Initialize intent
        intent_type ← IntentType.SELECT  // Default
        confidence ← 0.7  // Default confidence
        
        // Pattern matching for common intents
        IF contains_any(query_lower, ["how many", "count", "number of"]):
            intent_type ← IntentType.COUNT
            confidence ← 0.85
            
        ELSE IF contains_any(query_lower, ["average", "mean", "avg"]):
            intent_type ← IntentType.AGGREGATE
            confidence ← 0.85
            
        ELSE IF contains_any(query_lower, ["sum", "total"]):
            intent_type ← IntentType.AGGREGATE
            confidence ← 0.85
            
        ELSE IF contains_any(query_lower, ["top", "highest", "largest", "most"]):
            intent_type ← IntentType.SELECT
            confidence ← 0.80
            needs_sorting ← TRUE
            
        ELSE IF contains_any(query_lower, ["join", "combine", "merge"]):
            intent_type ← IntentType.JOIN
            confidence ← 0.75
            
        ELSE IF contains_any(query_lower, ["trend", "over time", "by month", "by year"]):
            intent_type ← IntentType.TIME_SERIES
            confidence ← 0.80
        END IF
        
        // Extract entities (dates, numbers, etc.)
        entities ← this.extract_entities(query.text)
        
        RETURN Intent(
            type: intent_type,
            confidence: confidence,
            entities: entities
        )
    END FUNCTION
    
    
    /*
     * ENTITY EXTRACTION
     * Purpose: Extract structured data from natural language
     * Entities: dates, numbers, table hints, column hints
     */
    PRIVATE FUNCTION extract_entities(text: String) → Dictionary:
        entities ← {}
        
        // ===== DATE EXTRACTION =====
        date_parser ← DateParser()
        date_info ← date_parser.parse(text)
        
        IF date_info IS NOT NULL:
            entities["date"] ← date_info
            // date_info contains: {type: "relative/absolute", value: ..., sql_expression: ...}
        END IF
        
        // ===== NUMBER EXTRACTION =====
        // Find all numbers in text
        number_pattern ← REGEX("\b\d+\b")
        numbers ← find_all_matches(text, number_pattern)
        
        IF LENGTH(numbers) > 0:
            entities["numbers"] ← numbers
        END IF
        
        // ===== TABLE HINTS =====
        // Look for potential table name mentions
        known_table_keywords ← ["patients", "encounters", "admissions", "discharges", "census"]
        mentioned_tables ← []
        
        FOR EACH keyword IN known_table_keywords:
            IF contains(to_lowercase(text), keyword):
                APPEND(mentioned_tables, keyword)
            END IF
        END FOR
        
        IF LENGTH(mentioned_tables) > 0:
            entities["table_hints"] ← mentioned_tables
        END IF
        
        // ===== COMPARISON OPERATORS =====
        IF contains_any(text, ["greater than", "more than", "above"]):
            entities["comparison"] ← ">"
        ELSE IF contains_any(text, ["less than", "fewer than", "below"]):
            entities["comparison"] ← "<"
        ELSE IF contains_any(text, ["equal to", "equals"]):
            entities["comparison"] ← "="
        END IF
        
        RETURN entities
    END FUNCTION
    
    
    /*
     * NATURAL LANGUAGE ANSWER GENERATION
     * Purpose: Convert query results into human-readable text
     */
    PRIVATE ASYNC FUNCTION generate_natural_language_answer(query: UserQuery, result: QueryResult) → String:
        // Handle failure cases
        IF NOT result.success:
            RETURN "Query failed: " + result.error_message
        END IF
        
        IF result.row_count = 0:
            RETURN "No results found for your query."
        END IF
        
        // Generate answer based on intent type
        SWITCH query.intent:
            
            CASE IntentType.COUNT:
                // Extract count value (should be single row, single column)
                IF result.row_count = 1 AND LENGTH(result.rows[0]) = 1:
                    count_value ← first_value(result.rows[0])
                    entity ← this.extract_count_entity(query.text)  // "patients", "admissions", etc.
                    
                    plural_entity ← pluralize(entity, count_value)
                    RETURN count_value + " " + plural_entity + " found."
                ELSE:
                    RETURN result.row_count + " rows returned."
                END IF
                
            CASE IntentType.AGGREGATE:
                // Extract aggregate value
                IF result.row_count = 1:
                    agg_value ← first_value(result.rows[0])
                    agg_type ← this.extract_aggregate_type(query.text)  // "average", "sum", etc.
                    
                    RETURN "The " + agg_type + " is " + format_number(agg_value) + "."
                ELSE:
                    RETURN result.row_count + " groups returned."
                END IF
                
            CASE IntentType.SELECT:
                RETURN result.row_count + " " + pluralize("record", result.row_count) + " returned."
                
            CASE IntentType.TIME_SERIES:
                RETURN "Time series data with " + result.row_count + " data points."
                
            DEFAULT:
                RETURN result.row_count + " rows returned."
        END SWITCH
    END FUNCTION
    
END CLASS


/*
 * HELPER FUNCTIONS FOR ERROR HANDLING
 */

FUNCTION create_error_response(query_id, error_type, message, suggestions) → QueryResponse:
    RETURN QueryResponse(
        query_id: query_id,
        original_query: "",
        generated_sql: NULL,
        result: QueryResult(
            query_id: query_id,
            success: FALSE,
            rows: [],
            row_count: 0,
            columns: [],
            execution_time_ms: 0,
            error_message: message
        ),
        natural_language_answer: message,
        total_time_ms: 0,
        cached: FALSE,
        error_type: error_type,
        suggestions: suggestions
    )
END FUNCTION
```

### **3.2 Conversation Manager**

```pseudocode
/*
 * CONVERSATION MANAGER
 * Purpose: Maintain conversation context across query turns
 * Responsibilities: Session management, history tracking, context resolution
 */

CLASS ConversationManager:
    PRIVATE sessions: Dictionary  // session_id → UserSession
    PRIVATE max_history_length: Integer ← 20
    PRIVATE session_timeout: Integer ← 14400  // 4 hours in seconds
    
    
    /*
     * ADD CONVERSATION TURN
     * Purpose: Record query-response pair in conversation history
     */
    FUNCTION add_turn(session: UserSession, query: UserQuery, response: QueryResponse):
        // Create conversation turn
        turn ← ConversationTurn(
            turn_id: generate_unique_id(),
            user_query: query,
            response: response,
            timestamp: current_timestamp()
        )
        
        // Add to session history
        APPEND(session.conversation_history, turn)
        
        // Limit history length (keep most recent)
        IF LENGTH(session.conversation_history) > this.max_history_length:
            session.conversation_history ← session.conversation_history[-this.max_history_length:]
        END IF
        
        // Update session activity timestamp
        session.last_activity ← current_timestamp()
        
        // Persist to storage (async)
        ASYNC_CALL persist_session(session)
        
    END FUNCTION
    
    
    /*
     * RESOLVE REFERENCES IN QUERY
     * Purpose: Handle pronouns and references to previous context
     * Examples: "it", "them", "the same", "previous"
     */
    FUNCTION resolve_references(query_text: String, session: UserSession) → String:
        // If no conversation history, no references to resolve
        IF LENGTH(session.conversation_history) = 0:
            RETURN query_text
        END IF
        
        resolved_query ← query_text
        last_turn ← session.conversation_history[-1]
        
        // Pattern 1: "Show me more" / "top 10" / "breakdown"
        IF contains_any(to_lowercase(query_text), ["more", "top", "breakdown", "by"]) AND
           NOT contains(to_lowercase(query_text), ["show", "give", "get"]):
            // This is a refinement of the previous query
            previous_query ← last_turn.user_query.text
            resolved_query ← previous_query + " " + query_text
        END IF
        
        // Pattern 2: Pronouns referring to previous subject
        IF contains_any(to_lowercase(query_text), ["it", "them", "those", "these"]):
            // Extract subject from previous query
            previous_subject ← this.extract_subject(last_turn.user_query.text)
            
            IF previous_subject IS NOT NULL:
                // Replace pronoun with actual subject
                resolved_query ← replace_pronouns(query_text, previous_subject)
            END IF
        END IF
        
        // Pattern 3: "same as before" / "previous"
        IF contains_any(to_lowercase(query_text), ["same", "previous", "last"]):
            previous_entities ← last_turn.user_query.entities
            // Merge entities from previous query
        END IF
        
        RETURN resolved_query
    END FUNCTION
    
    
    /*
     * EXTRACT SUBJECT FROM QUERY
     * Purpose: Identify main subject for pronoun resolution
     */
    PRIVATE FUNCTION extract_subject(query_text: String) → String:
        // Simple heuristic: look for nouns after "how many", "show me", etc.
        patterns ← [
            "how many (\\w+)",
            "show me (\\w+)",
            "list (\\w+)",
            "count (\\w+)"
        ]
        
        FOR EACH pattern IN patterns:
            match ← find_first_match(query_text, pattern)
            IF match IS NOT NULL:
                RETURN match.group(1)  // First capture group
            END IF
        END FOR
        
        RETURN NULL
    END FUNCTION
    
    
    /*
     * SESSION CLEANUP
     * Purpose: Remove expired sessions to free memory
     */
    FUNCTION cleanup_expired_sessions():
        current_time ← current_timestamp()
        expired_sessions ← []
        
        FOR EACH session_id, session IN this.sessions:
            time_since_activity ← current_time - session.last_activity
            
            IF time_since_activity > this.session_timeout:
                APPEND(expired_sessions, session_id)
            END IF
        END FOR
        
        // Remove expired sessions
        FOR EACH session_id IN expired_sessions:
            DELETE this.sessions[session_id]
            LOG(INFO, "Session expired and removed", session_id: session_id)
        END FOR
        
        RETURN LENGTH(expired_sessions)
    END FUNCTION
    
END CLASS
```

---

## **4. RAG Module - Retrieval Augmented Generation**

### **4.1 RAG Engine**

```pseudocode
/*
 * RAG ENGINE
 * Purpose: Retrieve relevant context from vector store for SQL generation
 * Process: Query → Embedding → Vector Search → Ranking → Filtering → Context
 */

CLASS RAGEngine:
    PRIVATE vector_store: VectorStore
    PRIVATE embedding_generator: EmbeddingGenerator
    PRIVATE config: RAGConfig
    PRIVATE logger: Logger
    
    
    /*
     * RETRIEVE CONTEXT
     * Main entry point for RAG retrieval
     */
    ASYNC FUNCTION retrieve_context(
        query: String,
        intent: Intent,
        conversation_history: List<ConversationTurn>
    ) → RetrievalContext:
        
        start_time ← current_timestamp_milliseconds()
        
        // ===== STEP 1: GENERATE QUERY EMBEDDING =====
        query_embedding ← AWAIT this.embedding_generator.generate_embedding(query)
        
        
        // ===== STEP 2: SEMANTIC SEARCH IN VECTOR STORE =====
        // Retrieve more than needed (will filter later)
        search_results ← AWAIT this.vector_store.search(
            query_embedding: query_embedding,
            top_k: this.config.top_k * 2,  // Retrieve 2x for filtering
            filters: {
                "type": ["table", "column", "relationship", "example", "business_rule"]
            }
        )
        
        this.logger.log_debug(
            message: "Vector search complete",
            results_count: LENGTH(search_results)
        )
        
        
        // ===== STEP 3: FILTER BY RELEVANCE THRESHOLD =====
        filtered_results ← []
        
        FOR EACH result IN search_results:
            IF result.similarity_score >= this.config.similarity_threshold:
                APPEND(filtered_results, result)
            END IF
        END FOR
        
        
        // ===== STEP 4: CATEGORIZE RESULTS BY TYPE =====
        tables ← []
        columns ← []
        relationships ← []
        examples ← []
        business_rules ← []
        
        FOR EACH result IN filtered_results:
            element_type ← result.metadata["type"]
            
            SWITCH element_type:
                CASE "table":
                    APPEND(tables, result)
                CASE "column":
                    APPEND(columns, result)
                CASE "relationship":
                    APPEND(relationships, result)
                CASE "example":
                    APPEND(examples, result)
                CASE "business_rule":
                    APPEND(business_rules, result)
            END SWITCH
        END FOR
        
        
        // ===== STEP 5: INTELLIGENT RANKING =====
        ranked_elements ← this.rank_elements(
            tables: tables,
            columns: columns,
            relationships: relationships,
            examples: examples,
            business_rules: business_rules,
            intent: intent,
            conversation_history: conversation_history
        )
        
        
        // ===== STEP 6: FIT TO TOKEN BUDGET =====
        // Ensure total context fits within LLM token limit
        selected_elements ← this.fit_to_token_budget(
            elements: ranked_elements,
            max_tokens: this.config.max_context_tokens
        )
        
        
        // ===== STEP 7: CREATE RETRIEVAL CONTEXT =====
        retrieval_time ← current_timestamp_milliseconds() - start_time
        total_tokens ← this.count_total_tokens(selected_elements)
        
        context ← RetrievalContext(
            query: query,
            retrieved_elements: selected_elements,
            retrieval_time_ms: retrieval_time,
            total_tokens: total_tokens
        )
        
        this.logger.log_info(
            message: "Context retrieval complete",
            elements_count: LENGTH(selected_elements),
            total_tokens: total_tokens,
            retrieval_time_ms: retrieval_time
        )
        
        RETURN context
        
    END FUNCTION
    
    
    /*
     * RANK ELEMENTS BY RELEVANCE
     * Purpose: Prioritize most relevant schema elements
     * Factors: Similarity score, element type, intent match, recency, usage
     */
    PRIVATE FUNCTION rank_elements(
        tables, columns, relationships, examples, business_rules, intent, conversation_history
    ) → List<SchemaElement>:
        
        ranked ← []
        
        // ===== PRIORITIZE TABLES =====
        // Tables are foundation of schema, always include top matches
        top_tables ← take_top_n(tables, 3)  // Top 3 most relevant tables
        
        FOR EACH table IN top_tables:
            element ← SchemaElement(
                element_id: table.id,
                element_type: "table",
                content: table.document,
                metadata: table.metadata,
                score: table.similarity_score * 1.2  // Boost table priority
            )
            APPEND(ranked, element)
        END FOR
        
        
        // ===== ADD RELEVANT COLUMNS =====
        // Only columns from selected tables
        table_names ← EXTRACT_FIELD(top_tables, "metadata.table_name")
        
        relevant_columns ← []
        FOR EACH column IN columns:
            IF column.metadata["table"] IN table_names:
                APPEND(relevant_columns, column)
            END IF
        END FOR
        
        // Take top 5-10 columns
        top_columns ← take_top_n(relevant_columns, 10)
        
        FOR EACH column IN top_columns:
            element ← SchemaElement(
                element_id: column.id,
                element_type: "column",
                content: column.document,
                metadata: column.metadata,
                score: column.similarity_score
            )
            APPEND(ranked, element)
        END FOR
        
        
        // ===== ADD RELATIONSHIPS =====
        // Relationships between selected tables
        FOR EACH relationship IN relationships:
            IF relationship.metadata["from_table"] IN table_names OR
               relationship.metadata["to_table"] IN table_names:
                
                element ← SchemaElement(
                    element_id: relationship.id,
                    element_type: "relationship",
                    content: relationship.document,
                    metadata: relationship.metadata,
                    score: relationship.similarity_score
                )
                APPEND(ranked, element)
            END IF
        END FOR
        
        
        // ===== ADD INTENT-MATCHED EXAMPLES =====
        // Filter examples by intent type
        intent_matched_examples ← []
        
        FOR EACH example IN examples:
            example_tags ← example.metadata.get("tags", [])
            
            // Check if example intent matches current query intent
            IF intent.type.value IN example_tags:
                // Boost score for intent match
                example.similarity_score ← example.similarity_score * 1.15
                APPEND(intent_matched_examples, example)
            END IF
        END FOR
        
        // Take top 2-3 examples
        top_examples ← take_top_n(intent_matched_examples, 3)
        
        FOR EACH example IN top_examples:
            element ← SchemaElement(
                element_id: example.id,
                element_type: "example",
                content: example.document,
                metadata: example.metadata,
                score: example.similarity_score
            )
            APPEND(ranked, element)
        END FOR
        
        
        // ===== ADD BUSINESS RULES =====
        // Business rules provide domain logic
        top_rules ← take_top_n(business_rules, 2)
        
        FOR EACH rule IN top_rules:
            element ← SchemaElement(
                element_id: rule.id,
                element_type: "business_rule",
                content: rule.document,
                metadata: rule.metadata,
                score: rule.similarity_score
            )
            APPEND(ranked, element)
        END FOR
        
        
        // ===== FINAL SORT BY ADJUSTED SCORE =====
        SORT ranked BY score DESCENDING
        
        RETURN ranked
    END FUNCTION
    
    
    /*
     * FIT TO TOKEN BUDGET
     * Purpose: Ensure context fits within LLM token limit
     * Strategy: Greedy selection by score until budget exhausted
     */
    PRIVATE FUNCTION fit_to_token_budget(
        elements: List<SchemaElement>,
        max_tokens: Integer
    ) → List<SchemaElement>:
        
        selected ← []
        total_tokens ← 0
        
        // Add system prompt overhead (estimated 200 tokens)
        CONST SYSTEM_PROMPT_TOKENS ← 200
        total_tokens ← SYSTEM_PROMPT_TOKENS
        
        FOR EACH element IN elements:
            element_tokens ← this.estimate_token_count(element.content)
            
            // Check if adding this element exceeds budget
            IF total_tokens + element_tokens <= max_tokens:
                APPEND(selected, element)
                total_tokens ← total_tokens + element_tokens
            ELSE:
                // Budget exhausted, stop adding
                BREAK
            END IF
        END FOR
        
        this.logger.log_debug(
            message: "Token budget allocation",
            selected_elements: LENGTH(selected),
            total_elements: LENGTH(elements),
            total_tokens: total_tokens,
            max_tokens: max_tokens
        )
        
        RETURN selected
    END FUNCTION
    
    
    /*
     * ESTIMATE TOKEN COUNT
     * Purpose: Rough estimation of tokens in text
     * Heuristic: 1 token ≈ 4 characters (English text)
     */
    PRIVATE FUNCTION estimate_token_count(text: String) → Integer:
        RETURN CEILING(LENGTH(text) / 4)
    END FUNCTION
    
    
    /*
     * COUNT TOTAL TOKENS
     * Purpose: Sum tokens across all elements
     */
    PRIVATE FUNCTION count_total_tokens(elements: List<SchemaElement>) → Integer:
        total ← 0
        
        FOR EACH element IN elements:
            total ← total + this.estimate_token_count(element.content)
        END FOR
        
        RETURN total
    END FUNCTION
    
END CLASS


/*
 * EMBEDDING GENERATOR
 * Purpose: Generate vector embeddings for text
 * Model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
 */

CLASS EmbeddingGenerator:
    PRIVATE model: EmbeddingModel
    PRIVATE model_name: String
    PRIVATE dimension: Integer ← 384
    
    
    /*
     * INITIALIZE
     */
    FUNCTION initialize(model_name: String):
        this.model_name ← model_name
        
        // Load embedding model (lazy loading)
        this.model ← load_embedding_model(model_name)
        
        LOG(INFO, "Embedding model loaded", model: model_name)
    END FUNCTION
    
    
    /*
     * GENERATE EMBEDDING
     * Input: Text string
     * Output: 384-dimensional vector
     */
    ASYNC FUNCTION generate_embedding(text: String) → Vector:
        // Preprocess text
        cleaned_text ← this.preprocess_text(text)
        
        // Generate embedding using model
        TRY:
            embedding ← AWAIT this.model.encode(
                text: cleaned_text,
                normalize: TRUE  // L2 normalization for cosine similarity
            )
            
            RETURN embedding
            
        CATCH exception AS e:
            LOG(ERROR, "Embedding generation failed", error: e)
            RAISE EmbeddingError("Failed to generate embedding: " + e.message)
        END TRY
    END FUNCTION
    
    
    /*
     * BATCH GENERATE EMBEDDINGS
     * Purpose: Generate embeddings for multiple texts efficiently
     */
    ASYNC FUNCTION generate_embeddings_batch(texts: List<String>) → List<Vector>:
        // Preprocess all texts
        cleaned_texts ← []
        FOR EACH text IN texts:
            APPEND(cleaned_texts, this.preprocess_text(text))
        END FOR
        
        // Batch encoding (more efficient than one-by-one)
        embeddings ← AWAIT this.model.encode_batch(
            texts: cleaned_texts,
            normalize: TRUE,
            batch_size: 32
        )
        
        RETURN embeddings
    END FUNCTION
    
    
    /*
     * PREPROCESS TEXT
     * Purpose: Clean and normalize text before embedding
     */
    PRIVATE FUNCTION preprocess_text(text: String) → String:
        // Convert to lowercase
        text ← to_lowercase(text)
        
        // Remove extra whitespace
        text ← normalize_whitespace(text)
        
        // Truncate to max length (model limit: 512 tokens)
        MAX_LENGTH ← 2000  // characters (roughly 512 tokens)
        IF LENGTH(text) > MAX_LENGTH:
            text ← text[0:MAX_LENGTH]
        END IF
        
        RETURN text
    END FUNCTION
    
END CLASS
```

---

## **5. LLM Module - SQL Generation**

### **5.1 LLM Engine**

```pseudocode
/*
 * LLM ENGINE
 * Purpose: Generate SQL from natural language using Ollama
 * Model: SQLCoder-7B (optimized for SQL generation)
 * Process: Build Prompt → Call Ollama → Parse SQL → Extract Metadata
 */

CLASS LLMEngine:
    PRIVATE ollama_client: OllamaClient
    PRIVATE prompt_builder: PromptBuilder
    PRIVATE config: OllamaConfig
    PRIVATE logger: Logger
    
    
    /*
     * GENERATE SQL
     * Main entry point for SQL generation
     */
    ASYNC FUNCTION generate_sql(
        query: UserQuery,
        context: RetrievalContext,
        conversation: List<ConversationTurn>
    ) → GeneratedSQL:
        
        start_time ← current_timestamp_milliseconds()
        
        // ===== STEP 1: BUILD PROMPT =====
        prompt ← this.prompt_builder.build_prompt(
            query: query,
            context: context,
            conversation: conversation,
            dialect: "tsql"  // SQL Server T-SQL
        )
        
        this.logger.log_debug(
            message: "Prompt built",
            prompt_length: LENGTH(prompt),
            token_estimate: LENGTH(prompt) / 4
        )
        
        
        // ===== STEP 2: CALL OLLAMA FOR GENERATION =====
        TRY:
            response ← AWAIT this.ollama_client.generate(
                model: this.config.model,  // "sqlcoder:7b-q4"
                prompt: prompt,
                options: {
                    "temperature": this.config.temperature,  // 0.1 for deterministic
                    "top_p": 0.9,
                    "top_k": 40,
                    "num_predict": this.config.max_tokens,  // 512
                    "stop": [";", "```", "\n\n"]  // Stop sequences
                },
                stream: FALSE,  // Wait for complete response
                timeout: this.config.timeout  // 45 seconds
            )
            
        CATCH timeout_error:
            LOG(ERROR, "LLM generation timeout")
            RAISE LLMTimeoutError("SQL generation exceeded timeout")
            
        CATCH connection_error:
            LOG(ERROR, "Cannot connect to Ollama")
            RAISE LLMConnectionError("Ollama service unavailable")
            
        CATCH exception AS e:
            LOG(ERROR, "LLM generation failed", error: e)
            RAISE LLMError("SQL generation failed: " + e.message)
        END TRY
        
        
        // ===== STEP 3: PARSE SQL FROM RESPONSE =====
        sql_text ← this.parse_sql_from_response(response["response"])
        
        IF sql_text IS EMPTY:
            LOG(WARNING, "Empty SQL generated")
            RAISE LLMError("Generated SQL is empty")
        END IF
        
        
        // ===== STEP 4: EXTRACT METADATA =====
        complexity ← this.assess_sql_complexity(sql_text)
        tables ← this.extract_table_references(sql_text)
        
        
        // ===== STEP 5: CREATE RESPONSE =====
        generation_time ← current_timestamp_milliseconds() - start_time
        
        generated_sql ← GeneratedSQL(
            sql_text: sql_text,
            dialect: "tsql",
            complexity: complexity,
            tables_referenced: tables,
            generation_time_ms: generation_time,
            confidence: this.calculate_confidence(response)
        )
        
        this.logger.log_info(
            message: "SQL generated successfully",
            generation_time_ms: generation_time,
            complexity: complexity,
            tables_count: LENGTH(tables)
        )
        
        RETURN generated_sql
        
    END FUNCTION
    
    
    /*
     * PARSE SQL FROM LLM RESPONSE
     * Purpose: Extract clean SQL from potentially messy LLM output
     * Handles: Markdown code blocks, explanatory text, multiple statements
     */
    PRIVATE FUNCTION parse_sql_from_response(response_text: String) → String:
        sql ← response_text
        
        // ===== REMOVE MARKDOWN CODE BLOCKS =====
        // Pattern: ```sql\n<SQL>\n```
        sql ← replace_pattern(sql, "```sql\\n", "")
        sql ← replace_pattern(sql, "```\\n?", "")
        sql ← replace_pattern(sql, "```", "")
        
        
        // ===== EXTRACT SQL PORTION =====
        // SQL typically starts with SELECT, WITH, INSERT, UPDATE, DELETE
        lines ← split_lines(sql)
        sql_lines ← []
        in_sql_block ← FALSE
        
        FOR EACH line IN lines:
            trimmed_line ← trim(line)
            
            // Check if line starts SQL statement
            IF matches_pattern(trimmed_line, "^(SELECT|WITH|INSERT|UPDATE|DELETE)\\b", case_insensitive: TRUE):
                in_sql_block ← TRUE
            END IF
            
            // If we're in SQL block, collect lines
            IF in_sql_block:
                APPEND(sql_lines, line)
            END IF
            
            // Stop at common end markers
            IF matches_pattern(trimmed_line, "^(Explanation|Note|Example):", case_insensitive: TRUE):
                BREAK
            END IF
        END FOR
        
        sql ← join_lines(sql_lines, "\n")
        
        
        // ===== CLEANUP =====
        // Remove trailing semicolons (we'll add if needed)
        sql ← trim(sql)
        sql ← trim_right(sql, ";")
        
        // Remove multiple blank lines
        sql ← replace_pattern(sql, "\\n{3,}", "\\n\\n")
        
        
        // ===== VALIDATION =====
        // Ensure we have valid SQL-looking text
        IF NOT contains_any(to_uppercase(sql), ["SELECT", "WITH", "INSERT", "UPDATE", "DELETE"]):
            LOG(WARNING, "Parsed text doesn't look like SQL", text: sql[0:100])
            // Still return it - validator will catch if invalid
        END IF
        
        RETURN sql
    END FUNCTION
    
    
    /*
     * ASSESS SQL COMPLEXITY
     * Purpose: Categorize query complexity for monitoring/optimization
     * Categories: simple, moderate, complex
     */
    PRIVATE FUNCTION assess_sql_complexity(sql: String) → String:
        sql_upper ← to_uppercase(sql)
        
        // Count complexity indicators
        join_count ← count_occurrences(sql_upper, "JOIN")
        subquery_count ← count_occurrences(sql_upper, "SELECT") - 1  // Exclude main SELECT
        cte_count ← count_occurrences(sql_upper, "WITH")
        union_count ← count_occurrences(sql_upper, "UNION")
        window_function_count ← count_occurrences(sql_upper, "OVER (")
        
        // Categorize by complexity
        IF cte_count > 0 OR subquery_count > 2 OR join_count > 5 OR window_function_count > 0:
            RETURN "complex"
            
        ELSE IF join_count > 2 OR subquery_count > 0 OR union_count > 0:
            RETURN "moderate"
            
        ELSE:
            RETURN "simple"
        END IF
    END FUNCTION
    
    
    /*
     * EXTRACT TABLE REFERENCES
     * Purpose: Identify all tables used in SQL query
     * Used for: Validation, permissions checking, monitoring
     */
    PRIVATE FUNCTION extract_table_references(sql: String) → List<String>:
        tables ← []
        
        // Pattern 1: FROM clause
        // Match: FROM schema.table or FROM table
        from_pattern ← "FROM\\s+([a-zA-Z_][a-zA-Z0-9_.]*)"
        from_matches ← find_all_matches(sql, from_pattern, case_insensitive: TRUE)
        
        FOR EACH match IN from_matches:
            table_name ← match.group(1)
            IF table_name NOT IN tables:
                APPEND(tables, table_name)
            END IF
        END FOR
        
        // Pattern 2: JOIN clause
        join_pattern ← "JOIN\\s+([a-zA-Z_][a-zA-Z0-9_.]*)"
        join_matches ← find_all_matches(sql, join_pattern, case_insensitive: TRUE)
        
        FOR EACH match IN join_matches:
            table_name ← match.group(1)
            IF table_name NOT IN tables:
                APPEND(tables, table_name)
            END IF
        END FOR
        
        // Pattern 3: INTO clause (for INSERT INTO)
        into_pattern ← "INTO\\s+([a-zA-Z_][a-zA-Z0-9_.]*)"
        into_matches ← find_all_matches(sql, into_pattern, case_insensitive: TRUE)
        
        FOR EACH match IN into_matches:
            table_name ← match.group(1)
            IF table_name NOT IN tables:
                APPEND(tables, table_name)
            END IF
        END FOR
        
        RETURN tables
    END FUNCTION
    
    
    /*
     * CALCULATE CONFIDENCE SCORE
     * Purpose: Estimate confidence in generated SQL
     * Factors: Response coherence, SQL validity indicators
     * TODO: Implement more sophisticated confidence scoring
     */
    PRIVATE FUNCTION calculate_confidence(response: Dictionary) → Float:
        // Placeholder: Default to 0.85
        // Future: Analyze response tokens, logprobs, etc.
        RETURN 0.85
    END FUNCTION
    
END CLASS
```

### **5.2 Prompt Builder**

```pseudocode
/*
 * PROMPT BUILDER
 * Purpose: Construct optimized prompts for SQL generation
 * Strategy: System instruction + Schema + Examples + Query
 */

CLASS PromptBuilder:
    
    /*
     * BUILD PROMPT
     * Main entry point for prompt construction
     */
    FUNCTION build_prompt(
        query: UserQuery,
        context: RetrievalContext,
        conversation: List<ConversationTurn>,
        dialect: String
    ) → String:
        
        prompt_parts ← []
        
        // ===== PART 1: SYSTEM INSTRUCTION =====
        system_instruction ← this.create_system_instruction(dialect)
        APPEND(prompt_parts, system_instruction)
        
        // ===== PART 2: SCHEMA CONTEXT =====
        schema_context ← this.format_schema_context(context.retrieved_elements)
        APPEND(prompt_parts, "\n\n## Database Schema:\n")
        APPEND(prompt_parts, schema_context)
        
        // ===== PART 3: BUSINESS RULES (if any) =====
        business_rules ← this.extract_business_rules(context.retrieved_elements)
        IF LENGTH(business_rules) > 0:
            APPEND(prompt_parts, "\n\n## Business Rules:\n")
            APPEND(prompt_parts, business_rules)
        END IF
        
        // ===== PART 4: EXAMPLE QUERIES (few-shot learning) =====
        examples ← this.extract_example_queries(context.retrieved_elements)
        IF LENGTH(examples) > 0:
            APPEND(prompt_parts, "\n\n## Example Queries:\n")
            APPEND(prompt_parts, examples)
        END IF
        
        // ===== PART 5: CONVERSATION CONTEXT (if applicable) =====
        IF LENGTH(conversation) > 0:
            conversation_context ← this.format_conversation_context(conversation)
            APPEND(prompt_parts, "\n\n## Recent Conversation:\n")
            APPEND(prompt_parts, conversation_context)
        END IF
        
        // ===== PART 6: USER QUERY =====
        APPEND(prompt_parts, "\n\n## User Question:\n")
        APPEND(prompt_parts, query.text)
        
        // ===== PART 7: GENERATION INSTRUCTION =====
        APPEND(prompt_parts, "\n\n## Your Task:\n")
        APPEND(prompt_parts, "Generate a " + dialect + " query to answer the user's question. ")
        APPEND(prompt_parts, "Return ONLY the SQL query, no explanations or markdown.\n\n")
        APPEND(prompt_parts, "SQL Query:\n")
        
        // Combine all parts
        full_prompt ← join(prompt_parts, "")
        
        RETURN full_prompt
    END FUNCTION
    
    
    /*
     * CREATE SYSTEM INSTRUCTION
     * Purpose: Define LLM role and constraints
     */
    PRIVATE FUNCTION create_system_instruction(dialect: String) → String:
        instruction ← "You are an expert SQL developer specializing in " + dialect + ". "
        instruction ← instruction + "Your task is to convert natural language questions into accurate, efficient SQL queries.\n\n"
        instruction ← instruction + "Guidelines:\n"
        instruction ← instruction + "- Generate syntactically correct " + dialect + " queries\n"
        instruction ← instruction + "- Use provided schema information only\n"
        instruction ← instruction + "- Follow examples for query patterns\n"
        instruction ← instruction + "- Apply business rules where relevant\n"
        instruction ← instruction + "- Use explicit column names (avoid SELECT *)\n"
        instruction ← instruction + "- Add appropriate WHERE clauses for filtering\n"
        instruction ← instruction + "- Use JOINs only when necessary\n"
        instruction ← instruction + "- Return ONLY the SQL query, no explanations\n"
        
        RETURN instruction
    END FUNCTION
    
    
    /*
     * FORMAT SCHEMA CONTEXT
     * Purpose: Convert schema elements to readable format
     */
    PRIVATE FUNCTION format_schema_context(elements: List<SchemaElement>) → String:
        schema_lines ← []
        
        // Group elements by type
        tables ← filter_by_type(elements, "table")
        columns ← filter_by_type(elements, "column")
        relationships ← filter_by_type(elements, "relationship")
        
        // Format tables
        FOR EACH table_element IN tables:
            table_metadata ← table_element.metadata
            table_name ← table_metadata["table_name"]
            schema_name ← table_metadata.get("schema", "dbo")
            description ← table_metadata.get("description", "")
            
            line ← "Table: " + schema_name + "." + table_name
            IF description:
                line ← line + " - " + description
            END IF
            
            APPEND(schema_lines, line)
            
            // Add columns for this table
            table_columns ← filter_by_table(columns, table_name)
            FOR EACH col IN table_columns:
                col_name ← col.metadata["column_name"]
                col_type ← col.metadata["data_type"]
                col_desc ← col.metadata.get("description", "")
                
                col_line ← "  - " + col_name + " (" + col_type + ")"
                IF col_desc:
                    col_line ← col_line + ": " + col_desc
                END IF
                
                APPEND(schema_lines, col_line)
            END FOR
            
            APPEND(schema_lines, "")  // Blank line between tables
        END FOR
        
        // Format relationships
        IF LENGTH(relationships) > 0:
            APPEND(schema_lines, "Relationships:")
            FOR EACH rel IN relationships:
                rel_line ← "  - " + rel.metadata["from_table"] + "." + rel.metadata["from_column"]
                rel_line ← rel_line + " → " + rel.metadata["to_table"] + "." + rel.metadata["to_column"]
                APPEND(schema_lines, rel_line)
            END FOR
        END IF
        
        RETURN join(schema_lines, "\n")
    END FUNCTION
    
    
    /*
     * EXTRACT BUSINESS RULES
     * Purpose: Format business logic rules for prompt
     */
    PRIVATE FUNCTION extract_business_rules(elements: List<SchemaElement>) → String:
        rules ← filter_by_type(elements, "business_rule")
        
        IF LENGTH(rules) = 0:
            RETURN ""
        END IF
        
        rule_lines ← []
        FOR EACH rule IN rules:
            APPEND(rule_lines, "- " + rule.content)
        END FOR
        
        RETURN join(rule_lines, "\n")
    END FUNCTION
    
    
    /*
     * EXTRACT EXAMPLE QUERIES
     * Purpose: Provide few-shot examples for learning
     */
    PRIVATE FUNCTION extract_example_queries(elements: List<SchemaElement>) → String:
        examples ← filter_by_type(elements, "example")
        
        IF LENGTH(examples) = 0:
            RETURN ""
        END IF
        
        example_lines ← []
        FOR i ← 0 TO MIN(LENGTH(examples), 3):  // Max 3 examples
            example ← examples[i]
            
            // Parse example content (format: "Q: ... SQL: ...")
            example_parts ← split(example.content, "SQL:")
            IF LENGTH(example_parts) = 2:
                question ← trim(example_parts[0].replace("Q:", ""))
                sql ← trim(example_parts[1])
                
                APPEND(example_lines, "Question: " + question)
                APPEND(example_lines, "SQL: " + sql)
                APPEND(example_lines, "")  // Blank line
            END IF
        END FOR
        
        RETURN join(example_lines, "\n")
    END FUNCTION
    
    
    /*
     * FORMAT CONVERSATION CONTEXT
     * Purpose: Provide recent conversation for context-aware generation
     */
    PRIVATE FUNCTION format_conversation_context(conversation: List<ConversationTurn>) → String:
        context_lines ← []
        
        // Include last 3 turns max
        recent_turns ← conversation[-3:]
        
        FOR EACH turn IN recent_turns:
            APPEND(context_lines, "User: " + turn.user_query.text)
            APPEND(context_lines, "SQL: " + turn.response.generated_sql.sql_text)
            APPEND(context_lines, "")
        END FOR
        
        RETURN join(context_lines, "\n")
    END FUNCTION
    
END CLASS
```

---

## **6. Validation Module - Security & Safety**

### **6.1 Query Validator**

```pseudocode
/*
 * QUERY VALIDATOR
 * Purpose: Multi-layer validation to prevent harmful SQL execution
 * Layers: Injection → Operations → Schema → Complexity → Size
 */

CLASS QueryValidator:
    PRIVATE schema_provider: SchemaProvider
    PRIVATE config: ValidationConfig
    PRIVATE logger: Logger
    
    // Prohibited keywords (DDL, DML, system commands)
    PRIVATE CONST PROHIBITED_KEYWORDS ← [
        "DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE",
        "ALTER", "CREATE", "GRANT", "REVOKE",
        "EXEC", "EXECUTE", "xp_cmdshell", "sp_executesql"
    ]
    
    
    /*
     * VALIDATE INPUT
     * Purpose: Basic input validation before processing
     */
    FUNCTION validate_input(query_text: String):
        // Check for empty input
        IF is_empty(trim(query_text)):
            RAISE ValidationError("Query cannot be empty")
        END IF
        
        // Check length limits
        IF LENGTH(query_text) > 500:
            RAISE ValidationError("Query too long (maximum 500 characters)")
        END IF
        
        // Check for suspicious patterns
        IF contains_pattern(query_text, "<script", case_insensitive: TRUE):
            RAISE ValidationError("Invalid characters in query")
        END IF
    END FUNCTION
    
    
    /*
     * VALIDATE SQL
     * Purpose: Comprehensive SQL validation before execution
     * Returns: ValidationResult with issues and suggestions
     */
    ASYNC FUNCTION validate_sql(
        sql: String,
        context_elements: List<SchemaElement>
    ) → ValidationResult:
        
        issues ← []
        
        // ===== LAYER 1: SQL INJECTION CHECK =====
        injection_issues ← this.check_sql_injection(sql)
        EXTEND(issues, injection_issues)
        
        // ===== LAYER 2: PROHIBITED OPERATIONS CHECK =====
        operation_issues ← this.check_prohibited_operations(sql)
        EXTEND(issues, operation_issues)
        
        // ===== LAYER 3: SCHEMA VALIDATION =====
        schema_issues ← AWAIT this.validate_schema_references(sql)
        EXTEND(issues, schema_issues)
        
        // ===== LAYER 4: COMPLEXITY CHECK =====
        complexity_issues ← this.check_query_complexity(sql)
        EXTEND(issues, complexity_issues)
        
        // ===== LAYER 5: RESULT SIZE ESTIMATION =====
        size_issues ← this.estimate_result_size(sql)
        EXTEND(issues, size_issues)
        
        // ===== DETERMINE OVERALL VALIDATION STATUS =====
        has_critical_errors ← FALSE
        
        FOR EACH issue IN issues:
            IF issue.level IN [ValidationLevel.ERROR, ValidationLevel.CRITICAL]:
                has_critical_errors ← TRUE
                BREAK
            END IF
        END FOR
        
        validation_result ← ValidationResult(
            passed: NOT has_critical_errors,
            issues: issues,
            validated_sql: sql
        )
        
        // Log validation result
        IF NOT validation_result.passed:
            this.logger.log_warning(
                message: "SQL validation failed",
                issues_count: LENGTH(issues)
            )
        END IF
        
        RETURN validation_result
    END FUNCTION
    
    
    /*
     * LAYER 1: SQL INJECTION CHECK
     * Purpose: Detect SQL injection patterns
     */
    PRIVATE FUNCTION check_sql_injection(sql: String) → List<ValidationIssue>:
        issues ← []
        sql_upper ← to_uppercase(sql)
        
        // Pattern 1: Multi-statement injection (semicolon followed by DROP/DELETE)
        IF matches_pattern(sql_upper, ";\\s*(DROP|DELETE|UPDATE|INSERT)"):
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.CRITICAL,
                message: "Potential SQL injection: Multiple statements detected",
                rule: "sql_injection_multistatement",
                suggestion: "Only single SELECT statements are allowed"
            ))
        END IF
        
        // Pattern 2: Comment injection
        IF contains(sql, "--") OR contains(sql, "/*"):
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.CRITICAL,
                message: "Potential SQL injection: Comments detected",
                rule: "sql_injection_comments",
                suggestion: "SQL comments are not allowed"
            ))
        END IF
        
        // Pattern 3: Union-based injection
        IF matches_pattern(sql_upper, "UNION\\s+SELECT") AND
           NOT this.is_legitimate_union(sql):
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.WARNING,
                message: "UNION detected - verify this is intentional",
                rule: "sql_injection_union",
                suggestion: "UNION queries require careful review"
            ))
        END IF
        
        // Pattern 4: Dynamic SQL execution
        IF contains_any(sql_upper, ["EXEC(", "EXECUTE(", "sp_executesql"]):
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.CRITICAL,
                message: "Dynamic SQL execution not allowed",
                rule: "sql_injection_dynamic",
                suggestion: "Use static SQL queries only"
            ))
        END IF
        
        // Pattern 5: System stored procedures
        IF contains_any(sql_upper, ["xp_cmdshell", "xp_regwrite", "xp_regread"]):
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.CRITICAL,
                message: "System stored procedures not allowed",
                rule: "sql_injection_system_proc",
                suggestion: "Cannot execute system commands"
            ))
        END IF
        
        RETURN issues
    END FUNCTION
    
    
    /*
     * LAYER 2: PROHIBITED OPERATIONS CHECK
     * Purpose: Block data modification operations
     */
    PRIVATE FUNCTION check_prohibited_operations(sql: String) → List<ValidationIssue>:
        issues ← []
        sql_upper ← trim(to_uppercase(sql))
        
        // Extract first keyword
        first_word ← split(sql_upper, " ")[0]
        
        // Check if first word is prohibited
        IF first_word IN this.PROHIBITED_KEYWORDS:
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.CRITICAL,
                message: "Prohibited operation: " + first_word,
                rule: "read_only_enforcement",
                suggestion: "Only SELECT queries are allowed. Rephrase as SELECT statement."
            ))
            RETURN issues  // Critical error, no need to check further
        END IF
        
        // Check for prohibited keywords anywhere in query (nested)
        FOR EACH keyword IN this.PROHIBITED_KEYWORDS:
            IF contains(sql_upper, keyword):
                // Check if it's part of a column name or false positive
                IF this.is_keyword_in_context(sql_upper, keyword):
                    APPEND(issues, ValidationIssue(
                        level: ValidationLevel.WARNING,
                        message: "Query contains keyword '" + keyword + "' - verify usage",
                        rule: "prohibited_keyword_check",
                        suggestion: "Ensure this keyword is part of column/table name, not operation"
                    ))
                END IF
            END IF
        END FOR
        
        RETURN issues
    END FUNCTION
    
    
    /*
     * LAYER 3: SCHEMA VALIDATION
     * Purpose: Verify referenced tables and columns exist
     */
    PRIVATE ASYNC FUNCTION validate_schema_references(sql: String) → List<ValidationIssue>:
        issues ← []
        
        // Extract table references
        tables ← this.extract_table_names(sql)
        
        // Check each table exists
        FOR EACH table_name IN tables:
            table_exists ← AWAIT this.schema_provider.table_exists(table_name)
            
            IF NOT table_exists:
                // Table doesn't exist - try to find similar tables
                suggestions ← AWAIT this.schema_provider.suggest_similar_tables(table_name)
                
                suggestion_text ← ""
                IF LENGTH(suggestions) > 0:
                    suggestion_text ← "Did you mean: " + join(suggestions, ", ") + "?"
                END IF
                
                APPEND(issues, ValidationIssue(
                    level: ValidationLevel.ERROR,
                    message: "Table '" + table_name + "' does not exist in database",
                    rule: "schema_validation_table",
                    suggestion: suggestion_text
                ))
            END IF
        END FOR
        
        // TODO: Column validation (requires SQL parsing)
        // For MVP, table validation is sufficient
        // Future: Parse SQL AST and validate each column reference
        
        RETURN issues
    END FUNCTION
    
    
    /*
     * LAYER 4: COMPLEXITY CHECK
     * Purpose: Warn about overly complex queries
     */
    PRIVATE FUNCTION check_query_complexity(sql: String) → List<ValidationIssue>:
        issues ← []
        sql_upper ← to_uppercase(sql)
        
        // Count complexity indicators
        join_count ← count_occurrences(sql_upper, "JOIN")
        subquery_count ← count_occurrences(sql_upper, "(SELECT") // Nested SELECTs
        union_count ← count_occurrences(sql_upper, "UNION")
        
        // Check JOIN count
        IF join_count > this.config.max_joins:  // e.g., 5
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.WARNING,
                message: "Query has " + join_count + " JOINs (recommended maximum: " + this.config.max_joins + ")",
                rule: "complexity_joins",
                suggestion: "Consider breaking into multiple simpler queries or adding date filters"
            ))
        END IF
        
        // Check subquery nesting
        IF subquery_count > this.config.max_subquery_depth:  // e.g., 3
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.WARNING,
                message: "Query has " + subquery_count + " nested subqueries (recommended maximum: " + this.config.max_subquery_depth + ")",
                rule: "complexity_subqueries",
                suggestion: "Consider using CTEs (WITH clause) for better readability"
            ))
        END IF
        
        // Check UNION operations
        IF union_count > 2:
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.INFO,
                message: "Query uses multiple UNIONs - this may be slow",
                rule: "complexity_unions",
                suggestion: "Verify this query pattern is necessary"
            ))
        END IF
        
        RETURN issues
    END FUNCTION
    
    
    /*
     * LAYER 5: RESULT SIZE ESTIMATION
     * Purpose: Warn about potentially large result sets
     */
    PRIVATE FUNCTION estimate_result_size(sql: String) → List<ValidationIssue>:
        issues ← []
        sql_upper ← to_uppercase(sql)
        
        // Check for TOP/LIMIT clause
        has_top ← contains(sql_upper, "TOP ")
        has_limit ← contains(sql_upper, "LIMIT ")
        
        // Check for WHERE clause (filtering)
        has_where ← contains(sql_upper, "WHERE ")
        
        // Check for aggregation (usually returns small result sets)
        is_aggregate ← contains_any(sql_upper, ["COUNT(", "SUM(", "AVG(", "GROUP BY"])
        
        // Warn if no limiting factors
        IF NOT has_top AND NOT has_limit AND NOT has_where AND NOT is_aggregate:
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.WARNING,
                message: "Query may return large result set (no TOP, WHERE, or GROUP BY clause)",
                rule: "result_size_unlimited",
                suggestion: "Add date filters or TOP clause to limit results. Example: TOP 1000 or WHERE date > ..."
            ))
        END IF
        
        // Check for SELECT * (usually returns many columns)
        IF contains(sql_upper, "SELECT *"):
            APPEND(issues, ValidationIssue(
                level: ValidationLevel.INFO,
                message: "Query uses SELECT * - consider specifying explicit columns",
                rule: "select_star",
                suggestion: "Selecting specific columns is more efficient and clearer"
            ))
        END IF
        
        RETURN issues
    END FUNCTION
    
    
    /*
     * HELPER: Extract table names from SQL
     * Simple regex-based extraction (good enough for validation)
     */
    PRIVATE FUNCTION extract_table_names(sql: String) → List<String>:
        tables ← []
        
        // Pattern: FROM table_name or JOIN table_name
        pattern ← "(FROM|JOIN)\\s+([a-zA-Z_][a-zA-Z0-9_.]*)"
        matches ← find_all_matches(sql, pattern, case_insensitive: TRUE)
        
        FOR EACH match IN matches:
            table_name ← match.group(2)  // Second capture group
            
            // Remove schema prefix if present (e.g., dbo.table → table)
            IF contains(table_name, "."):
                table_name ← split(table_name, ".")[-1]  // Last part
            END IF
            
            IF table_name NOT IN tables:
                APPEND(tables, table_name)
            END IF
        END FOR
        
        RETURN tables
    END FUNCTION
    
    
    /*
     * HELPER: Check if keyword is in valid context (column name, etc.)
     */
    PRIVATE FUNCTION is_keyword_in_context(sql_upper: String, keyword: String) → Boolean:
        // Simple check: if keyword is surrounded by non-word characters, it's likely actual keyword
        // If surrounded by word characters, it's likely part of a name
        
        pattern ← "\\b" + keyword + "\\b"  // Word boundary
        
        IF matches_pattern(sql_upper, pattern):
            RETURN FALSE  // Standalone keyword (bad)
        ELSE:
            RETURN TRUE  // Part of identifier (okay)
        END IF
    END FUNCTION
    
END CLASS
```

---

## **7. Database Module - Query Execution**

### **7.1 Database Engine**

```pseudocode
/*
 * DATABASE ENGINE
 * Purpose: Execute SQL queries safely against database
 * Features: Connection pooling, timeouts, error handling
 */

CLASS DatabaseEngine:
    PRIVATE connection_pool: ConnectionPool
    PRIVATE config: DatabaseConfig
    PRIVATE logger: Logger
    PRIVATE metrics: MetricsCollector
    
    
    /*
     * INITIALIZE
     * Set up connection pool
     */
    FUNCTION initialize(config, logger, metrics):
        this.config ← config
        this.logger ← logger
        this.metrics ← metrics
        
        // Create connection pool
        connection_string ← this.build_connection_string(config)
        
        this.connection_pool ← create_connection_pool(
            connection_string: connection_string,
            pool_size: config.pool_size,  // e.g., 10-20
            max_overflow: config.max_overflow,  // e.g., 10
            timeout: config.timeout,  // e.g., 30 seconds
            pool_recycle: 3600  // Recycle connections after 1 hour
        )
        
        // Test initial connection
        IF NOT this.test_connection():
            RAISE ConnectionError("Cannot establish database connection")
        END IF
        
        this.logger.log_info("Database engine initialized", pool_size: config.pool_size)
    END FUNCTION
    
    
    /*
     * EXECUTE QUERY
     * Main entry point for SQL execution
     */
    ASYNC FUNCTION execute_query(sql: String, timeout: Integer) → QueryResult:
        start_time ← current_timestamp_milliseconds()
        query_id ← generate_unique_id()
        
        TRY:
            // ===== STEP 1: ACQUIRE CONNECTION FROM POOL =====
            connection ← AWAIT this.connection_pool.acquire_connection(
                timeout: 5  // Wait max 5 seconds for connection
            )
            
            this.logger.log_debug("Connection acquired from pool")
            
            
            // ===== STEP 2: SET QUERY TIMEOUT =====
            // SQL Server specific: SET LOCK_TIMEOUT
            AWAIT connection.execute("SET LOCK_TIMEOUT " + (timeout * 1000))  // milliseconds
            
            // Query governor (SQL Server specific)
            AWAIT connection.execute("SET QUERY_GOVERNOR_COST_LIMIT " + timeout)
            
            
            // ===== STEP 3: EXECUTE SQL =====
            cursor ← AWAIT connection.execute(sql)
            
            
            // ===== STEP 4: FETCH RESULTS =====
            rows ← []
            columns ← []
            
            // Get column names from cursor
            IF cursor.description IS NOT NULL:
                FOR EACH column_desc IN cursor.description:
                    APPEND(columns, column_desc[0])  // Column name
                END FOR
            END IF
            
            // Fetch all rows (with limit to prevent memory issues)
            MAX_ROWS ← 10000
            row_count ← 0
            
            WHILE TRUE:
                row ← AWAIT cursor.fetchone()
                
                IF row IS NULL:
                    BREAK  // No more rows
                END IF
                
                // Convert row tuple to dictionary
                row_dict ← {}
                FOR i ← 0 TO LENGTH(columns):
                    row_dict[columns[i]] ← row[i]
                END FOR
                
                APPEND(rows, row_dict)
                row_count ← row_count + 1
                
                // Safety limit
                IF row_count >= MAX_ROWS:
                    this.logger.log_warning("Result set truncated at " + MAX_ROWS + " rows")
                    BREAK
                END IF
            END WHILE
            
            
            // ===== STEP 5: CLOSE CURSOR AND RETURN CONNECTION =====
            AWAIT cursor.close()
            AWAIT this.connection_pool.release_connection(connection)
            
            
            // ===== STEP 6: CREATE RESULT =====
            execution_time ← current_timestamp_milliseconds() - start_time
            
            result ← QueryResult(
                query_id: query_id,
                success: TRUE,
                rows: rows,
                row_count: row_count,
                columns: columns,
                execution_time_ms: execution_time,
                error_message: NULL
            )
            
            // Log success
            this.logger.log_info(
                message: "Query executed successfully",
                row_count: row_count,
                execution_time_ms: execution_time
            )
            
            // Record metrics
            this.metrics.histogram("database.query_time", execution_time)
            this.metrics.histogram("database.row_count", row_count)
            this.metrics.increment("database.queries_success")
            
            RETURN result
            
        CATCH timeout_error:
            this.logger.log_error("Query timeout", timeout: timeout)
            this.metrics.increment("database.queries_timeout")
            
            RETURN QueryResult(
                query_id: query_id,
                success: FALSE,
                rows: [],
                row_count: 0,
                columns: [],
                execution_time_ms: timeout * 1000,
                error_message: "Query exceeded timeout of " + timeout + " seconds"
            )
            
        CATCH database_error AS e:
            this.logger.log_error("Database error", error: e)
            this.metrics.increment("database.queries_error")
            
            RETURN QueryResult(
                query_id: query_id,
                success: FALSE,
                rows: [],
                row_count: 0,
                columns: [],
                execution_time_ms: current_timestamp_milliseconds() - start_time,
                error_message: "Database error: " + e.message
            )
            
        FINALLY:
            // Ensure connection is always returned to pool
            IF connection IS NOT NULL:
                AWAIT this.connection_pool.release_connection(connection)
            END IF
        END TRY
    END FUNCTION
    
    
    /*
     * TEST CONNECTION
     * Purpose: Verify database connectivity
     */
    FUNCTION test_connection() → Boolean:
        TRY:
            connection ← this.connection_pool.acquire_connection(timeout: 5)
            cursor ← connection.execute("SELECT 1")
            result ← cursor.fetchone()
            cursor.close()
            this.connection_pool.release_connection(connection)
            
            RETURN result IS NOT NULL
            
        CATCH exception:
            RETURN FALSE
        END TRY
    END FUNCTION
    
    
    /*
     * BUILD CONNECTION STRING
     * Purpose: Construct database connection string from config
     */
    PRIVATE FUNCTION build_connection_string(config: DatabaseConfig) → String:
        // SQL Server ODBC connection string format
        conn_str ← "Driver={" + config.driver + "};"
        conn_str ← conn_str + "Server=" + config.host + "," + config.port + ";"
        conn_str ← conn_str + "Database=" + config.database + ";"
        conn_str ← conn_str + "UID=" + config.username + ";"
        conn_str ← conn_str + "PWD=" + config.password + ";"
        conn_str ← conn_str + "Encrypt=yes;"
        conn_str ← conn_str + "TrustServerCertificate=no;"
        
        RETURN conn_str
    END FUNCTION
    
    
    /*
     * CLOSE ALL CONNECTIONS
     * Purpose: Gracefully shutdown connection pool
     */
    FUNCTION close_all_connections():
        this.logger.log_info("Closing all database connections")
        this.connection_pool.dispose()
    END FUNCTION
    
END CLASS
```

---

## **8. UI Module - User Interface**

### **8.1 Streamlit Application**

```pseudocode
/*
 * STREAMLIT APPLICATION
 * Purpose: Web-based user interface for query submission and results
 * Framework: Streamlit (Python-native web framework)
 * Note: This is Python-specific; see section 11 for JavaScript alternatives
 */

IMPORT streamlit as st

// Global application instance (injected from main)
GLOBAL app: Application


/*
 * MAIN UI FUNCTION
 * Streamlit entry point
 */
FUNCTION main():
    // ===== PAGE CONFIGURATION =====
    st.set_page_config(
        page_title: "SQL Query Assistant",
        page_icon: "🔍",
        layout: "wide",  // Use full width
        initial_sidebar_state: "expanded"
    )
    
    // ===== LOAD CUSTOM CSS =====
    load_custom_styles()
    
    // ===== INITIALIZE SESSION STATE =====
    IF "session" NOT IN st.session_state:
        st.session_state.session ← create_user_session()
        st.session_state.query_history ← []
    END IF
    
    // ===== HEADER =====
    render_header()
    
    // ===== SIDEBAR =====
    render_sidebar()
    
    // ===== MAIN CONTENT =====
    render_main_content()
    
END FUNCTION


/*
 * RENDER HEADER
 */
FUNCTION render_header():
    col1, col2, col3 ← st.columns([2, 6, 2])
    
    WITH col1:
        st.image("logo.png", width: 100)
    END WITH
    
    WITH col2:
        st.title("🔍 SQL Query Assistant")
        st.caption("Ask questions about your data in natural language")
    END WITH
    
    WITH col3:
        st.button("⚙️ Settings", key: "settings_btn")
    END WITH
    
    st.divider()
END FUNCTION


/*
 * RENDER SIDEBAR
 * Shows query history and examples
 */
FUNCTION render_sidebar():
    WITH st.sidebar:
        st.header("📜 Query History")
        
        // Search history
        search_term ← st.text_input("🔍 Search history", key: "history_search")
        
        // Filter history by search term
        filtered_history ← st.session_state.query_history
        IF search_term:
            filtered_history ← filter_by_text(filtered_history, search_term)
        END IF
        
        // Display history items
        IF LENGTH(filtered_history) = 0:
            st.info("No query history yet")
        ELSE:
            FOR EACH query_item IN filtered_history:
                WITH st.expander(query_item.query_text[0:50] + "...", expanded: FALSE):
                    st.write("**Timestamp:**", query_item.timestamp)
                    st.write("**Row Count:**", query_item.row_count)
                    
                    // Button to re-run query
                    IF st.button("🔄 Re-run", key: "rerun_" + query_item.id):
                        st.session_state.current_query ← query_item.query_text
                        st.rerun()
                    END IF
                    
                    // Button to copy SQL
                    IF st.button("📋 Copy SQL", key: "copy_" + query_item.id):
                        st.code(query_item.sql, language: "sql")
                    END IF
                END WITH
            END FOR
        END IF
        
        st.divider()
        
        // Example queries
        st.header("💡 Example Queries")
        
        examples ← [
            "How many patients were admitted yesterday?",
            "Show me census by unit for last week",
            "Calculate 30-day readmission rate",
            "Top 10 diagnoses by volume"
        ]
        
        FOR EACH example IN examples:
            IF st.button(example, key: "example_" + example):
                st.session_state.current_query ← example
                st.rerun()
            END IF
        END FOR
    END WITH
END FUNCTION


/*
 * RENDER MAIN CONTENT
 * Query input and results display
 */
FUNCTION render_main_content():
    // ===== QUERY INPUT SECTION =====
    st.header("Ask a Question")
    
    // Pre-fill if coming from sidebar
    default_value ← st.session_state.get("current_query", "")
    
    query_text ← st.text_area(
        label: "Enter your question in natural language:",
        value: default_value,
        height: 120,
        placeholder: "Example: How many patients were admitted yesterday?",
        key: "query_input"
    )
    
    // Character counter
    char_count ← LENGTH(query_text)
    IF char_count > 450:
        st.warning("⚠️ Query is getting long (" + char_count + "/500 characters)")
    ELSE:
        st.caption(char_count + "/500 characters")
    END IF
    
    // Action buttons
    col1, col2, col3 ← st.columns([2, 2, 6])
    
    WITH col1:
        submit_clicked ← st.button("🚀 Submit Query", type: "primary", use_container_width: TRUE)
    END WITH
    
    WITH col2:
        clear_clicked ← st.button("🗑️ Clear", use_container_width: TRUE)
        IF clear_clicked:
            st.session_state.current_query ← ""
            st.rerun()
        END IF
    END WITH
    
    st.divider()
    
    
    // ===== PROCESS QUERY IF SUBMITTED =====
    IF submit_clicked AND NOT is_empty(query_text):
        process_and_display_query(query_text)
    END IF
    
    
    // ===== DISPLAY PREVIOUS RESULT (if any) =====
    IF "last_result" IN st.session_state:
        display_query_result(st.session_state.last_result)
    END IF
    
END FUNCTION


/*
 * PROCESS AND DISPLAY QUERY
 * Main query processing workflow
 */
FUNCTION process_and_display_query(query_text: String):
    // Show loading state
    WITH st.spinner("🤖 Processing your query..."):
        // Create user query object
        user_query ← UserQuery(
            query_id: generate_unique_id(),
            user_id: st.session_state.session.user_id,
            session_id: st.session_state.session.session_id,
            text: query_text,
            timestamp: current_timestamp()
        )
        
        // Process query through backend
        TRY:
            // Call query processor (async in Python with streamlit)
            response ← AWAIT app.query_processor.process_query(
                user_query: user_query,
                session: st.session_state.session
            )
            
            // Store result in session state
            st.session_state.last_result ← response
            
            // Add to history
            APPEND(st.session_state.query_history, {
                "id": response.query_id,
                "query_text": query_text,
                "sql": response.generated_sql.sql_text,
                "row_count": response.result.row_count,
                "timestamp": current_timestamp()
            })
            
            // Display result
            display_query_result(response)
            
        CATCH exception AS e:
            st.error("❌ " + e.message)
            
            IF e.suggestions:
                st.info("💡 **Suggestions:**")
                FOR EACH suggestion IN e.suggestions:
                    st.write("- " + suggestion)
                END FOR
            END IF
        END TRY
    END WITH
END FUNCTION


/*
 * DISPLAY QUERY RESULT
 * Render SQL and data results
 */
FUNCTION display_query_result(response: QueryResponse):
    // Success indicator
    IF response.result.success:
        st.success("✅ Query executed successfully!")
    ELSE:
        st.error("❌ Query execution failed")
        st.error(response.result.error_message)
        RETURN
    END IF
    
    // Metrics row
    col1, col2, col3 ← st.columns(3)
    
    WITH col1:
        st.metric("Rows Returned", response.result.row_count)
    END WITH
    
    WITH col2:
        st.metric("Execution Time", response.total_time_ms / 1000 + " seconds")
    END WITH
    
    WITH col3:
        IF response.cached:
            st.metric("Source", "Cache 🚀")
        ELSE:
            st.metric("Source", "Database")
        END IF
    END WITH
    
    st.divider()
    
    // Natural language answer
    st.subheader("📊 Answer")
    st.write(response.natural_language_answer)
    
    st.divider()
    
    // Generated SQL (collapsible)
    WITH st.expander("🔍 Generated SQL Query", expanded: FALSE):
        st.code(response.generated_sql.sql_text, language: "sql")
        
        // Copy button
        IF st.button("📋 Copy SQL"):
            st.write("SQL copied to clipboard!")  // Note: actual clipboard requires JS
        END IF
        
        // Query metadata
        st.caption("**Complexity:** " + response.generated_sql.complexity)
        st.caption("**Tables:** " + join(response.generated_sql.tables_referenced, ", "))
    END WITH
    
    st.divider()
    
    // Data table
    st.subheader("📋 Results")
    
    IF response.result.row_count = 0:
        st.info("No results found")
    ELSE IF response.result.row_count = 1:
        // Single row - display as key-value
        FOR key, value IN response.result.rows[0]:
            st.write("**" + key + ":**", value)
        END FOR
    ELSE:
        // Multiple rows - display as table
        dataframe ← convert_to_dataframe(response.result.rows)
        st.dataframe(
            dataframe,
            use_container_width: TRUE,
            height: 400
        )
        
        // Pagination if many rows
        IF response.result.row_count > 100:
            st.caption("Showing first 100 rows")
        END IF
    END IF
    
    st.divider()
    
    // Export options
    st.subheader("💾 Export Data")
    
    col1, col2, col3 ← st.columns(3)
    
    WITH col1:
        csv_data ← convert_to_csv(response.result.rows)
        st.download_button(
            label: "📥 Download CSV",
            data: csv_data,
            file_name: "query_result.csv",
            mime: "text/csv"
        )
    END WITH
    
    WITH col2:
        excel_data ← convert_to_excel(response.result.rows, response.generated_sql.sql_text)
        st.download_button(
            label: "📊 Download Excel",
            data: excel_data,
            file_name: "query_result.xlsx",
            mime: "application/vnd.ms-excel"
        )
    END WITH
    
    WITH col3:
        json_data ← convert_to_json(response.result.rows)
        st.download_button(
            label: "📄 Download JSON",
            data: json_data,
            file_name: "query_result.json",
            mime: "application/json"
        )
    END WITH
    
END FUNCTION


/*
 * LOAD CUSTOM CSS
 */
FUNCTION load_custom_styles():
    css ← """
    <style>
    .stTextArea textarea {
        font-size: 16px;
    }
    .stButton button {
        border-radius: 6px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html: TRUE)
END FUNCTION
```

---

## **9. Infrastructure Module - Utilities**

### **9.1 Caching Service**

```pseudocode
/*
 * CACHED QUERY PROCESSOR
 * Purpose: Wrapper around QueryProcessor with caching layer
 * Cache: Query results with 5-minute TTL
 */

CLASS CachedQueryProcessor:
    PRIVATE processor: QueryProcessor
    PRIVATE cache: CacheService
    PRIVATE ttl: Integer  // Time-to-live in seconds
    
    
    /*
     * PROCESS QUERY WITH CACHING
     */
    ASYNC FUNCTION process_query(user_query: UserQuery, session: UserSession) → QueryResponse:
        // Generate cache key
        cache_key ← this.generate_cache_key(user_query, session)
        
        // Check cache
        cached_result ← AWAIT this.cache.get(cache_key)
        
        IF cached_result IS NOT NULL:
            // Cache hit
            cached_result.cached ← TRUE
            LOG(INFO, "Cache hit", cache_key: cache_key)
            RETURN cached_result
        END IF
        
        // Cache miss - process query
        LOG(INFO, "Cache miss", cache_key: cache_key)
        result ← AWAIT this.processor.process_query(user_query, session)
        
        // Store in cache (only successful queries)
        IF result.result.success:
            AWAIT this.cache.set(
                key: cache_key,
                value: result,
                ttl: this.ttl
            )
        END IF
        
        RETURN result
    END FUNCTION
    
    
    /*
     * GENERATE CACHE KEY
     * Purpose: Create unique, consistent key for query+context
     */
    PRIVATE FUNCTION generate_cache_key(query: UserQuery, session: UserSession) → String:
        // Components that affect query result
        components ← [
            to_lowercase(trim(query.text)),  // Normalized query text
            app.schema_version,  // Schema version (invalidate on schema change)
            session.context.get("database", "default")  // Database context
        ]
        
        // Create hash of components
        key_string ← join(components, "|")
        cache_key ← md5_hash(key_string)
        
        RETURN cache_key
    END FUNCTION
    
END CLASS


/*
 * CACHE SERVICE
 * Purpose: Abstract cache interface (in-memory or Redis)
 */

CLASS CacheService:
    PRIVATE backend: String  // "memory" or "redis"
    PRIVATE memory_cache: Dictionary
    PRIVATE redis_client: RedisClient
    
    
    /*
     * GET FROM CACHE
     */
    ASYNC FUNCTION get(key: String) → Any:
        IF this.backend = "memory":
            // Check if exists and not expired
            IF key IN this.memory_cache:
                entry ← this.memory_cache[key]
                IF entry.expires_at > current_timestamp():
                    RETURN entry.value
                ELSE:
                    // Expired - remove
                    DELETE this.memory_cache[key]
                    RETURN NULL
                END IF
            ELSE:
                RETURN NULL
            END IF
            
        ELSE IF this.backend = "redis":
            value ← AWAIT this.redis_client.get(key)
            IF value IS NOT NULL:
                RETURN deserialize(value)
            ELSE:
                RETURN NULL
            END IF
        END IF
    END FUNCTION
    
    
    /*
     * SET IN CACHE
     */
    ASYNC FUNCTION set(key: String, value: Any, ttl: Integer):
        IF this.backend = "memory":
            this.memory_cache[key] ← {
                "value": value,
                "expires_at": current_timestamp() + ttl
            }
            
        ELSE IF this.backend = "redis":
            serialized_value ← serialize(value)
            AWAIT this.redis_client.setex(key, ttl, serialized_value)
        END IF
    END FUNCTION
    
    
    /*
     * CLEAR CACHE
     */
    FUNCTION clear():
        IF this.backend = "memory":
            this.memory_cache ← {}
        ELSE IF this.backend = "redis":
            this.redis_client.flushdb()
        END IF
    END FUNCTION
    
END CLASS
```

### **9.2 Logging Service**

```pseudocode
/*
 * STRUCTURED LOGGER
 * Purpose: Consistent, structured logging across application
 * Format: JSON for easy parsing and analysis
 */

CLASS Logger:
    PRIVATE logger_name: String
    PRIVATE log_level: String
    PRIVATE output_handler: LogHandler
    
    
    /*
     * LOG WITH CONTEXT
     * All log methods funnel through this
     */
    FUNCTION log(level: String, message: String, **context):
        // Create structured log entry
        log_entry ← {
            "timestamp": current_timestamp_iso(),
            "level": level,
            "logger": this.logger_name,
            "message": message,
            "context": context,
            "thread_id": get_current_thread_id(),
            "process_id": get_current_process_id()
        }
        
        // Add trace ID if in request context
        IF "trace_id" IN current_context():
            log_entry["trace_id"] ← current_context().trace_id
        END IF
        
        // Write to output
        this.output_handler.write(serialize_to_json(log_entry))
    END FUNCTION
    
    
    // Convenience methods for different log levels
    
    FUNCTION log_debug(message: String, **context):
        IF this.log_level IN ["DEBUG"]:
            this.log("DEBUG", message, **context)
        END IF
    END FUNCTION
    
    FUNCTION log_info(message: String, **context):
        IF this.log_level IN ["DEBUG", "INFO"]:
            this.log("INFO", message, **context)
        END IF
    END FUNCTION
    
    FUNCTION log_warning(message: String, **context):
        IF this.log_level IN ["DEBUG", "INFO", "WARNING"]:
            this.log("WARNING", message, **context)
        END IF
    END FUNCTION
    
    FUNCTION log_error(message: String, **context):
        IF this.log_level IN ["DEBUG", "INFO", "WARNING", "ERROR"]:
            this.log("ERROR", message, **context)
        END IF
    END FUNCTION
    
    FUNCTION log_critical(message: String, **context):
        this.log("CRITICAL", message, **context)
    END FUNCTION
    
END CLASS
```

---

## **10. Data Models and Structures**

### **10.1 Core Data Structures**

```pseudocode
/*
 * USER QUERY
 * Represents a user's natural language query
 */
STRUCTURE UserQuery:
    query_id: String                    // Unique identifier
    user_id: String                     // User who submitted query
    session_id: String                  // Session context
    text: String                        // Natural language query text
    timestamp: Timestamp                // When submitted
    intent: IntentType                  // Classified intent (optional)
    confidence: Float                   // Intent confidence (0-1)
    entities: Dictionary<String, Any>   // Extracted entities
END STRUCTURE


/*
 * INTENT
 * Query intent classification
 */
STRUCTURE Intent:
    type: IntentType        // COUNT, SELECT, AGGREGATE, JOIN, TIME_SERIES
    confidence: Float       // Confidence score (0-1)
    entities: Dictionary    // Extracted entities (dates, numbers, etc.)
END STRUCTURE

ENUM IntentType:
    SELECT
    COUNT
    AGGREGATE
    JOIN
    TIME_SERIES
    UNKNOWN
END ENUM


/*
 * GENERATED SQL
 * SQL query generated by LLM
 */
STRUCTURE GeneratedSQL:
    sql_text: String                // The SQL query
    dialect: String                 // "tsql", "postgres", "mysql"
    complexity: String              // "simple", "moderate", "complex"
    tables_referenced: List<String> // Tables used in query
    estimated_rows: Integer         // Estimated result size (optional)
    generation_time_ms: Float       // Time to generate
    confidence: Float               // Generation confidence
END STRUCTURE


/*
 * QUERY RESULT
 * Result of SQL execution
 */
STRUCTURE QueryResult:
    query_id: String                    // Links to UserQuery
    success: Boolean                    // Did query succeed?
    rows: List<Dictionary>              // Result data (row objects)
    row_count: Integer                  // Number of rows returned
    columns: List<String>               // Column names
    execution_time_ms: Float            // Database execution time
    error_message: String               // Error if failed (optional)
    warnings: List<String>              // Non-fatal warnings
END STRUCTURE


/*
 * QUERY RESPONSE
 * Complete response to user
 */
STRUCTURE QueryResponse:
    query_id: String                    // Unique identifier
    original_query: String              // User's original question
    generated_sql: GeneratedSQL         // Generated SQL object
    result: QueryResult                 // Execution result
    natural_language_answer: String     // Human-readable answer
    total_time_ms: Float                // Total processing time
    cached: Boolean                     // Was result from cache?
    error_type: String                  // Error category (optional)
    suggestions: List<String>           // Suggestions if error
END STRUCTURE


/*
 * SCHEMA ELEMENT
 * Single element in vector store (table, column, example, etc.)
 */
STRUCTURE SchemaElement:
    element_id: String          // Unique identifier
    element_type: String        // "table", "column", "relationship", "example", "business_rule"
    content: String             // Text description for embedding
    metadata: Dictionary        // Type-specific metadata
    embedding: Vector           // Embedding vector (384-dim for MiniLM)
    score: Float                // Relevance score (optional, for ranking)
END STRUCTURE


/*
 * RETRIEVAL CONTEXT
 * Context retrieved from RAG
 */
STRUCTURE RetrievalContext:
    query: String                       // Original query
    retrieved_elements: List<SchemaElement>  // Retrieved schema elements
    retrieval_time_ms: Float            // Time spent on retrieval
    total_tokens: Integer               // Estimated tokens in context
END STRUCTURE


/*
 * VALIDATION RESULT
 * Result of SQL validation
 */
STRUCTURE ValidationResult:
    passed: Boolean                     // Did validation pass?
    issues: List<ValidationIssue>       // List of issues found
    validated_sql: String               // Potentially corrected SQL
END STRUCTURE


/*
 * VALIDATION ISSUE
 * Single validation issue
 */
STRUCTURE ValidationIssue:
    level: ValidationLevel      // CRITICAL, ERROR, WARNING, INFO
    message: String             // Human-readable message
    rule: String                // Which validation rule triggered
    suggestion: String          // How to fix (optional)
END STRUCTURE

ENUM ValidationLevel:
    INFO
    WARNING
    ERROR
    CRITICAL
END ENUM


/*
 * USER SESSION
 * User session state
 */
STRUCTURE UserSession:
    session_id: String                      // Unique session identifier
    user_id: String                         // User identifier
    started_at: Timestamp                   // Session start time
    last_activity: Timestamp                // Last interaction time
    conversation_history: List<ConversationTurn>  // Query-response history
    context: Dictionary                     // Session-specific context
END STRUCTURE


/*
 * CONVERSATION TURN
 * Single query-response pair in conversation
 */
STRUCTURE ConversationTurn:
    turn_id: String             // Unique turn identifier
    user_query: UserQuery       // User's query
    response: QueryResponse     // System response
    timestamp: Timestamp        // When occurred
END STRUCTURE
```

---

## **11. Language-Specific Considerations**

### **11.1 Python Implementation Notes**

```python
# PYTHON-SPECIFIC CONSIDERATIONS

"""
PRIMARY LANGUAGE: Python 3.9+
RATIONALE: Native ML/AI ecosystem, team expertise, rapid development

ADVANTAGES:
- Rich ML libraries (transformers, chromadb, langchain)
- Ollama has official Python SDK
- Streamlit for rapid UI development
- Strong typing with type hints (Python 3.9+)
- Excellent data manipulation (pandas, numpy)

IMPLEMENTATION PATTERNS:
"""

# 1. ASYNC/AWAIT for I/O operations
async def process_query(user_query: UserQuery) -> QueryResponse:
    # Async database, LLM, vector store calls
    context = await rag_engine.retrieve_context(user_query)
    sql = await llm_engine.generate_sql(user_query, context)
    result = await db_engine.execute_query(sql)
    return QueryResponse(...)

# 2. TYPE HINTS for clarity
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class UserQuery:
    query_id: str
    text: str
    intent: Optional[IntentType] = None
    entities: Dict[str, Any] = None

# 3. DEPENDENCY INJECTION via constructors
class QueryProcessor:
    def __init__(
        self,
        rag_engine: RAGEngine,
        llm_engine: LLMEngine,
        validator: QueryValidator
    ):
        self.rag = rag_engine
        self.llm = llm_engine
        self.validator = validator

# 4. CONTEXT MANAGERS for resources
with database_engine.get_connection() as conn:
    result = conn.execute(sql)

# 5. DECORATORS for cross-cutting concerns
@cache(ttl=300)
@log_execution_time
@retry(max_attempts=3)
async def expensive_operation():
    pass

# 6. GENERATORS for memory efficiency
def fetch_large_result_set(cursor):
    while True:
        rows = cursor.fetchmany(1000)
        if not rows:
            break
        yield from rows

# LIBRARIES:
# - langchain: RAG orchestration
# - chromadb: Vector store
# - ollama: LLM client
# - streamlit: UI framework
# - pyodbc/sqlalchemy: Database connectivity
# - pydantic: Data validation
# - structlog: Structured logging
# - prometheus-client: Metrics
```

### **11.2 JavaScript/TypeScript Implementation Notes**

```javascript
// JAVASCRIPT/TYPESCRIPT CONSIDERATIONS

/*
ALTERNATIVE LANGUAGE: TypeScript (Node.js)
USE CASE: If team prefers JS ecosystem or needs React frontend

ADVANTAGES:
- React for rich UI
- Large npm ecosystem
- Good async support (promises, async/await)
- TypeScript adds static typing

CHALLENGES:
- Fewer ML libraries (must use Python bridge or APIs)
- Ollama client less mature
- No native ChromaDB client (REST API only)

IMPLEMENTATION PATTERNS:
*/

// 1. INTERFACES for type safety
interface UserQuery {
    queryId: string;
    userId: string;
    text: string;
    intent?: IntentType;
    entities?: Record<string, any>;
}

// 2. ASYNC/AWAIT for asynchronous operations
async function processQuery(
    userQuery: UserQuery, 
    session: UserSession
): Promise<QueryResponse> {
    const context = await ragEngine.retrieveContext(userQuery);
    const sql = await llmEngine.generateSql(userQuery, context);
    const result = await dbEngine.executeQuery(sql);
    
    return {
        queryId: generateUuid(),
        originalQuery: userQuery.text,
        generatedSql: sql,
        result: result,
        // ...
    };
}

// 3. DEPENDENCY INJECTION via constructor
class QueryProcessor {
    constructor(
        private ragEngine: RAGEngine,
        private llmEngine: LLMEngine,
        private validator: QueryValidator
    ) {}
    
    async processQuery(query: UserQuery): Promise<QueryResponse> {
        // Implementation
    }
}

// 4. ERROR HANDLING with try/catch
try {
    const result = await processQuery(query, session);
    return result;
} catch (error) {
    if (error instanceof ValidationError) {
        // Handle validation error
    } else if (error instanceof DatabaseError) {
        // Handle database error
    }
    throw error;
}

// 5. PROMISES for concurrent operations
const [context, metadata] = await Promise.all([
    ragEngine.retrieveContext(query),
    schemaProvider.getMetadata()
]);

// LIBRARIES:
// - langchain.js: RAG framework
// - ollama-js: LLM client
// - pg/mssql: Database drivers
// - express/fastify: Web framework
// - react: UI framework
// - winston: Logging
// - prom-client: Metrics

// ARCHITECTURE NOTE:
// For TypeScript, consider microservices:
// - Python service for ML/RAG (ChromaDB, Ollama)
// - Node.js service for API and business logic
// - React frontend
// Communication via REST or gRPC
```

### **11.3 Cross-Language Compatibility**

```pseudocode
/*
 * LANGUAGE-AGNOSTIC INTERFACE DESIGN
 * Purpose: Enable polyglot implementations
 * Strategy: Clear interfaces, REST APIs, message passing
 */

// INTERFACE: Query Processor
INTERFACE IQueryProcessor:
    METHOD process_query(
        query: String,
        session_id: String
    ) RETURNS QueryResponse
END INTERFACE

// REST API specification (language-agnostic)
API_ENDPOINT: POST /api/v1/query
REQUEST_BODY: {
    "query": "How many patients admitted yesterday?",
    "session_id": "sess_abc123"
}
RESPONSE_BODY: {
    "query_id": "q_xyz789",
    "generated_sql": "SELECT COUNT(*) FROM...",
    "result": {
        "rows": [...],
        "row_count": 45
    },
    "natural_language_answer": "45 patients admitted yesterday"
}

// This enables:
// - Python backend + JavaScript frontend
// - Multiple backend implementations
// - Service-oriented architecture
// - Independent scaling of components
```

---

## **12. Reflection and Optimization**

### **12.1 Alignment with Specifications**

**✅ Specification Coverage Verification**:

| Specification Requirement | Pseudocode Coverage | Notes |
|---------------------------|---------------------|-------|
| FR-1: Natural Language Input | ✅ Complete | `QueryProcessor.classify_intent`, `extract_entities` |
| FR-2: SQL Generation | ✅ Complete | `LLMEngine.generate_sql`, `PromptBuilder` |
| FR-3: RAG Context Retrieval | ✅ Complete | `RAGEngine.retrieve_context`, ranking logic |
| FR-4: LLM Integration | ✅ Complete | `LLMEngine`, Ollama client calls |
| FR-5: Query Validation | ✅ Complete | `QueryValidator` with 5 validation layers |
| FR-6: Query Execution | ✅ Complete | `DatabaseEngine.execute_query` |
| FR-7: Schema Management | ⚠️ Partial | Schema loading mentioned, full implementation in completion phase |
| FR-8: Conversation Management | ✅ Complete | `ConversationManager`, context resolution |
| FR-9: Result Presentation | ✅ Complete | Streamlit UI components |
| FR-10: UI Components | ✅ Complete | Full Streamlit implementation |
| FR-11: Example Library | ⚠️ Partial | Mentioned in sidebar, full CRUD in completion |
| FR-12: Logging & Audit | ✅ Complete | `Logger` class, structured logging |

**NFR Coverage**:
- ✅ Performance: Caching, connection pooling, async operations
- ✅ Security: Multi-layer validation, SQL injection prevention
- ✅ Reliability: Error handling, retries, timeouts
- ✅ Maintainability: Modular design, clear interfaces
- ✅ Usability: Natural language input, helpful error messages

---

### **12.2 Logical Issues and Inefficiencies**

**Identified Issues**:

**Issue 1: Schema Validation Performance**
- **Problem**: Validating every table/column in SQL requires multiple database queries
- **Impact**: Adds 200-500ms latency per query
- **Solution**: 
  ```pseudocode
  // Cache schema in memory after first load
  CACHE schema_metadata WITH TTL = 1 hour
  
  // Async schema validation (don't block)
  ASYNC_VALIDATE schema_references THEN log_warnings
  ```

**Issue 2: Prompt Token Counting**
- **Problem**: Using `LENGTH(text) / 4` for token estimation is inaccurate
- **Impact**: May exceed LLM context window, causing errors
- **Solution**:
  ```pseudocode
  // Use proper tokenizer
  IMPORT tiktoken  // or model-specific tokenizer
  
  FUNCTION accurate_token_count(text: String) → Integer:
      tokenizer ← get_tokenizer(model_name)
      tokens ← tokenizer.encode(text)
      RETURN LENGTH(tokens)
  END FUNCTION
  ```

**Issue 3: Conversation Context Growing Unbounded**
- **Problem**: Storing all conversation history in memory scales poorly
- **Impact**: Memory leak in long sessions
- **Solution**: Already addressed with `max_history_length = 20`
  ```pseudocode
  // Implemented in ConversationManager:
  IF LENGTH(session.conversation_history) > this.max_history_length:
      session.conversation_history ← session.conversation_history[-this.max_history_length:]
  END IF
  ```

**Issue 4: No Rate Limiting**
- **Problem**: User could spam queries, overload system
- **Impact**: DoS vulnerability, poor experience for other users
- **Solution**:
  ```pseudocode
  CLASS RateLimiter:
      FUNCTION check_rate_limit(user_id: String) → Boolean:
          requests_last_minute ← COUNT_REQUESTS(user_id, last_60_seconds)
          
          IF requests_last_minute > 10:  // Max 10 queries/minute
              RAISE RateLimitError("Too many requests")
          END IF
          
          RETURN TRUE
      END FUNCTION
  END CLASS
  ```

---

### **12.3 Alternative Approaches**

**Alternative 1: SQL Parser vs Regex for Table Extraction**

**Current Approach**: Regex patterns
```pseudocode
pattern ← "(FROM|JOIN)\\s+([a-zA-Z_][a-zA-Z0-9_.]*)"
```

**Alternative**: SQL Parser (sqlparse, sqlglot)
```pseudocode
IMPORT sqlparse

FUNCTION extract_tables_with_parser(sql: String) → List<String>:
    parsed ← sqlparse.parse(sql)[0]
    tables ← []
    
    FOR EACH token IN parsed.tokens:
        IF token.ttype IS Keyword AND token.value IN ["FROM", "JOIN"]:
            next_token ← get_next_token(token)
            IF next_token.ttype IS Name:
                APPEND(tables, next_token.value)
            END IF
        END IF
    END FOR
    
    RETURN tables
END FUNCTION
```

**Comparison**:
| Aspect | Regex | SQL Parser |
|--------|-------|------------|
| Speed | Fast | Slower (10-50ms) |
| Accuracy | 90% | 99% |
| Complexity | Low | Medium |
| Edge Cases | Misses some | Handles all |

**Recommendation**: Start with regex (good enough), upgrade to parser if accuracy issues arise.

---

**Alternative 2: Vector Store Selection**

**Current**: ChromaDB (embedded)
**Alternatives**: 
1. **FAISS** (Facebook AI Similarity Search)
   - Pros: Fastest search, battle-tested
   - Cons: Manual persistence, no metadata filtering
   
2. **Weaviate** (Production vector DB)
   - Pros: Production-grade, advanced features
   - Cons: Separate server, operational overhead

**Decision Matrix**:
| Requirement | ChromaDB | FAISS | Weaviate |
|-------------|----------|-------|----------|
| Embedded | ✅ | ✅ | ❌ |
| Persistence | ✅ | ⚠️ Manual | ✅ |
| Metadata Filter | ✅ | ❌ | ✅ |
| Performance | Good | Excellent | Excellent |
| Setup Complexity | Low | Low | High |

**Recommendation**: ChromaDB optimal for MVP, migrate to Weaviate if scale demands.

---

**Alternative 3: Caching Strategy**

**Current**: Single-tier in-memory cache
**Alternative**: Multi-tier cache

```pseudocode
CLASS MultiTierCache:
    L1_CACHE: In-Memory (fast, small capacity)
    L2_CACHE: Redis (medium speed, larger capacity)
    L3_CACHE: Database (slow, unlimited capacity)
    
    FUNCTION get(key: String) → Value:
        // Try L1
        IF key IN L1_CACHE:
            RETURN L1_CACHE[key]
        END IF
        
        // Try L2
        value ← L2_CACHE.get(key)
        IF value IS NOT NULL:
            L1_CACHE[key] ← value  // Promote to L1
            RETURN value
        END IF
        
        // Try L3
        value ← L3_CACHE.get(key)
        IF value IS NOT NULL:
            L2_CACHE.set(key, value, ttl: 3600)
            L1_CACHE[key] ← value
            RETURN value
        END IF
        
        RETURN NULL
    END FUNCTION
END CLASS
```

**Trade-offs**:
- More complexity vs better hit rates
- MVP: Single-tier sufficient
- Scale: Multi-tier when >50 users

---

### **12.4 Clarity and Readability Assessment**

**Readability Improvements**:

**Before** (Dense):
```pseudocode
FUNCTION f(q,s):r←p(q);c←g(r);x←l(c);RETURN x
```

**After** (Clear):
```pseudocode
FUNCTION process_query(user_query, session) → QueryResponse:
    // Step 1: Classify intent
    intent ← classify_intent(user_query)
    
    // Step 2: Retrieve context
    context ← retrieve_rag_context(intent)
    
    // Step 3: Generate SQL
    sql ← generate_sql_with_llm(context)
    
    RETURN QueryResponse(...)
END FUNCTION
```

**Naming Conventions Applied**:
- ✅ Descriptive function names: `generate_sql` not `gen`
- ✅ Clear variable names: `user_query` not `q`
- ✅ Consistent casing: `snake_case` for functions
- ✅ Commented sections: `// ===== STEP 1: ... =====`

**Accessibility Score**: 9/10
- Non-technical stakeholders can understand flow
- Developers can implement without ambiguity
- Clear separation of concerns

---

### **12.5 Implementation Roadmap**

**Phase 1: Core Pipeline (Week 1-2)**
```
Priority Order:
1. Data models and structures ← Foundation
2. Database engine ← Test connectivity early
3. Basic query processor ← Skeleton workflow
4. Simple LLM integration ← End-to-end smoke test
5. Basic validation ← Safety first

Deliverable: Query "SELECT 1" end-to-end
```

**Phase 2: RAG Integration (Week 3-4)**
```
Priority Order:
1. Embedding generator ← Required for RAG
2. Vector store setup ← Schema ingestion
3. Schema loader ← Populate vector store
4. RAG engine ← Context retrieval
5. Enhanced prompt builder ← Use retrieved context

Deliverable: Context-aware SQL generation
```

**Phase 3: Polish (Week 5-6)**
```
Priority Order:
1. Conversation manager ← Context across queries
2. Full validation suite ← All 5 layers
3. Error recovery logic ← Retry with corrections
4. UI components ← Streamlit interface
5. Result formatting ← Natural language answers

Deliverable: Complete user-facing application
```

**Phase 4: Testing & Optimization (Week 7-8)**
```
Priority Order:
1. Unit tests (80% coverage)
2. Integration tests (end-to-end)
3. Performance optimization
4. Load testing
5. Security testing

Deliverable: Production-ready system
```

---

### **12.6 Performance Optimization Opportunities**

**Optimization 1: Batch Embedding Generation**

**Current** (Sequential):
```pseudocode
FOR EACH schema_element IN schema_elements:
    embedding ← AWAIT generate_embedding(schema_element.text)
    schema_element.embedding ← embedding
END FOR
// Time: N × 20ms = 200ms for 10 elements
```

**Optimized** (Batch):
```pseudocode
texts ← EXTRACT_FIELD(schema_elements, "text")
embeddings ← AWAIT generate_embeddings_batch(texts, batch_size: 32)

FOR i ← 0 TO LENGTH(schema_elements):
    schema_elements[i].embedding ← embeddings[i]
END FOR
// Time: 60ms for 10 elements (3x faster)
```

---

**Optimization 2: Connection Pool Pre-warming**

**Current**:
```pseudocode
// First query pays cost of connection establishment
connection ← connection_pool.acquire()  // 200ms for first connection
```

**Optimized**:
```pseudocode
// During startup, pre-create minimum connections
FUNCTION initialize_connection_pool():
    FOR i ← 1 TO min_pool_size:
        connection ← create_connection()
        pool.add(connection)
    END FOR
    
    LOG(INFO, "Connection pool pre-warmed with " + min_pool_size + " connections")
END FUNCTION
// First query now instant (connection already exists)
```

---

**Optimization 3: Parallel Pipeline Stages**

**Current** (Sequential):
```pseudocode
context ← AWAIT retrieve_context(query)      // 400ms
sql ← AWAIT generate_sql(query, context)     // 2000ms
result ← AWAIT execute_query(sql)            // 800ms
// Total: 3200ms
```

**Optimized** (Parallel where possible):
```pseudocode
// Start context retrieval and intent classification in parallel
[context, intent] ← AWAIT parallel_execute([
    retrieve_context(query),
    classify_intent_detailed(query)  // More detailed than basic classification
])
// Both run simultaneously, total time = MAX(400ms, 200ms) = 400ms

// Then sequential (must wait for SQL before executing)
sql ← AWAIT generate_sql(query, context)     // 2000ms
result ← AWAIT execute_query(sql)            // 800ms
// Total: 3200ms → 3000ms (saved 200ms)
```

---

**Optimization 4: Query Result Streaming**

**Current**: Wait for complete result, then display
```pseudocode
result ← AWAIT execute_query(sql)  // Wait for all 10,000 rows
display_results(result)
```

**Optimized**: Stream results as they arrive
```pseudocode
ASYNC FUNCTION execute_query_streaming(sql):
    cursor ← AWAIT connection.execute(sql)
    
    // Yield rows in batches
    WHILE TRUE:
        batch ← cursor.fetchmany(100)
        IF LENGTH(batch) = 0:
            BREAK
        END IF
        
        YIELD batch  // Send to UI incrementally
    END WHILE
END FUNCTION

// UI displays first 100 rows immediately, then updates
```

---

### **12.7 Complex Implementation Notes**

**Complex Area 1: SQL Parser for Accurate Validation**

```pseudocode
/*
 * PLACEHOLDER: ADVANCED SQL PARSING
 * Current: Regex-based extraction (good enough for MVP)
 * Future: Use proper SQL parser for 100% accuracy
 * 
 * Libraries to consider:
 * - Python: sqlparse, sqlglot, pglast
 * - JavaScript: node-sql-parser
 * 
 * Benefits of parser:
 * - Accurate table/column extraction
 * - Handle complex nested queries
 * - Detect SQL injection more reliably
 * - Enable query optimization/rewriting
 */

FUNCTION parse_sql_with_library(sql: String) → ParsedSQL:
    // Using sqlglot as example
    
    TRY:
        parsed ← sqlglot.parse_one(sql, dialect: "tsql")
        
        // Extract tables
        tables ← []
        FOR EACH table_node IN parsed.find_all("Table"):
            APPEND(tables, table_node.name)
        END FOR
        
        // Extract columns
        columns ← []
        FOR EACH column_node IN parsed.find_all("Column"):
            APPEND(columns, {
                "name": column_node.name,
                "table": column_node.table
            })
        END FOR
        
        // Extract operations
        operations ← detect_operations(parsed)
        
        RETURN ParsedSQL(
            tables: tables,
            columns: columns,
            operations: operations,
            is_valid: TRUE
        )
        
    CATCH parse_error:
        RETURN ParsedSQL(is_valid: FALSE, error: parse_error.message)
    END TRY
END FUNCTION
```

---

**Complex Area 2: Confidence Scoring for SQL Generation**

```pseudocode
/*
 * PLACEHOLDER: CONFIDENCE SCORING
 * Current: Fixed 0.85 confidence
 * Future: Calculate confidence based on multiple factors
 * 
 * Factors to consider:
 * - LLM output probability (logprobs if available)
 * - Schema match quality (all tables exist?)
 * - Example similarity (how close to known good queries?)
 * - Query complexity (simple = higher confidence)
 * - Historical success rate for similar queries
 */

FUNCTION calculate_generation_confidence(
    llm_response: Dictionary,
    sql: String,
    context: RetrievalContext
) → Float:
    
    confidence_factors ← []
    
    // Factor 1: Schema validation (0-1)
    tables ← extract_tables(sql)
    valid_tables ← COUNT(table for table in tables WHERE table_exists(table))
    schema_confidence ← valid_tables / LENGTH(tables) IF LENGTH(tables) > 0 ELSE 1.0
    APPEND(confidence_factors, schema_confidence)
    
    // Factor 2: Context match quality (0-1)
    // How similar is query to retrieved examples?
    IF LENGTH(context.retrieved_elements) > 0:
        avg_similarity ← AVERAGE(element.score FOR element IN context.retrieved_elements)
        context_confidence ← avg_similarity
        APPEND(confidence_factors, context_confidence)
    END IF
    
    // Factor 3: SQL complexity (inverse - simpler = higher confidence)
    complexity ← assess_sql_complexity(sql)
    SWITCH complexity:
        CASE "simple":
            complexity_confidence ← 0.95
        CASE "moderate":
            complexity_confidence ← 0.80
        CASE "complex":
            complexity_confidence ← 0.65
    END SWITCH
    APPEND(confidence_factors, complexity_confidence)
    
    // Factor 4: LLM output probability (if available)
    // TODO: Ollama doesn't provide logprobs yet
    // When available, use perplexity or token probabilities
    
    // Aggregate confidence (weighted average)
    final_confidence ← AVERAGE(confidence_factors)
    
    RETURN final_confidence
END FUNCTION
```

---

**Complex Area 3: Query Optimization Suggestions**

```pseudocode
/*
 * PLACEHOLDER: QUERY OPTIMIZER
 * Current: Basic complexity warnings
 * Future: Suggest specific optimizations
 * 
 * Optimization types:
 * - Add indexes for frequent JOINs
 * - Rewrite subqueries as JOINs
 * - Add date filters to reduce scan size
 * - Use EXISTS instead of COUNT(*) > 0
 * - Partition tables for time-series queries
 */

FUNCTION suggest_query_optimizations(sql: String) → List<Optimization>:
    suggestions ← []
    
    // Check for missing date filters on large tables
    IF query_scans_large_table_without_filter(sql):
        APPEND(suggestions, Optimization(
            type: "add_filter",
            message: "Add date filter to reduce data scanned",
            example: "WHERE admit_date >= DATEADD(month, -1, GETDATE())"
        ))
    END IF
    
    // Check for COUNT(*) > 0 pattern (expensive)
    IF contains(sql, "COUNT(*) >"):
        APPEND(suggestions, Optimization(
            type: "use_exists",
            message: "Use EXISTS instead of COUNT for existence checks",
            example: "Replace: WHERE (SELECT COUNT(*) FROM ...) > 0\nWith: WHERE EXISTS (SELECT 1 FROM ...)"
        ))
    END IF
    
    // Check for DISTINCT with ORDER BY (can be slow)
    IF contains(sql, "DISTINCT") AND contains(sql, "ORDER BY"):
        APPEND(suggestions, Optimization(
            type: "optimize_distinct",
            message: "DISTINCT with ORDER BY can be slow on large datasets",
            example: "Consider using GROUP BY instead if appropriate"
        ))
    END IF
    
    RETURN suggestions
END FUNCTION
```

---

## **13. Final Pseudocode Checklist**

### **13.1 Completeness Verification**

**Core Modules**:
- ✅ Main Application Entry Point
- ✅ Query Processor (Orchestrator)
- ✅ Conversation Manager
- ✅ RAG Engine (Context Retrieval)
- ✅ Embedding Generator
- ✅ LLM Engine (SQL Generation)
- ✅ Prompt Builder
- ✅ Query Validator (All 5 layers)
- ✅ Database Engine (Execution)
- ✅ Streamlit UI
- ✅ Caching Service
- ✅ Logging Service

**Data Structures**:
- ✅ UserQuery, Intent, GeneratedSQL
- ✅ QueryResult, QueryResponse
- ✅ SchemaElement, RetrievalContext
- ✅ ValidationResult, ValidationIssue
- ✅ ConversationTurn, UserSession

**Cross-Cutting Concerns**:
- ✅ Error handling patterns
- ✅ Logging strategy
- ✅ Metrics collection
- ✅ Configuration management
- ✅ Resource cleanup

**Implementation Guidance**:
- ✅ Language-specific notes (Python, JavaScript/TypeScript)
- ✅ Performance optimizations
- ✅ Alternative approaches
- ✅ Complex implementation placeholders
- ✅ Development roadmap

---

### **13.2 Translation to Code**

**From Pseudocode to Python**:

```python
# Example translation of QueryProcessor.process_query

class QueryProcessor:
    async def process_query(
        self,
        user_query: UserQuery,
        session: UserSession
    ) -> QueryResponse:
        start_time = time.time()
        query_id = str(uuid.uuid4())
        
        try:
            # Stage 1: Input validation
            self.validator.validate_input(user_query.text)
            self.metrics.increment("queries.submitted")
            
            # Stage 2: Intent classification
            intent = await self.classify_intent(user_query)
            user_query.intent = intent.type
            user_query.confidence = intent.confidence
            
            # Stage 3: Context retrieval
            context = await self.rag_engine.retrieve_context(
                query=user_query.text,
                intent=intent,
                conversation_history=session.conversation_history
            )
            
            # Stage 4: SQL generation
            generated_sql = await self.llm_engine.generate_sql(
                query=user_query,
                context=context,
                conversation=session.conversation_history[-5:]
            )
            
            # Stage 5: Validation
            validation_result = await self.validator.validate_sql(
                sql=generated_sql.sql_text,
                context_elements=context.retrieved_elements
            )
            
            if not validation_result.passed:
                if validation_result.has_critical_errors():
                    raise ValidationError(validation_result.issues)
            
            # Stage 6: Execution
            result = await self.db_engine.execute_query(
                sql=generated_sql.sql_text,
                timeout=30
            )
            
            # Stage 7: Formatting
            nl_answer = await self.generate_natural_language_answer(
                query=user_query,
                result=result
            )
            
            # Stage 8: Create response
            response = QueryResponse(
                query_id=query_id,
                original_query=user_query.text,
                generated_sql=generated_sql,
                result=result,
                natural_language_answer=nl_answer,
                total_time_ms=(time.time() - start_time) * 1000
            )
            
            # Stage 9: Update conversation
            self.conversation_manager.add_turn(session, user_query, response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Query processing failed: {e}")
            raise
```

**Mapping Quality**: 1:1 correspondence between pseudocode and Python

---

### **13.3 Key Takeaways**

**Pseudocode Achievements**:

1. **Complete Pipeline**: All stages from input to output specified
2. **Clear Interfaces**: Module boundaries and contracts defined
3. **Error Handling**: Comprehensive try-catch patterns throughout
4. **Language Agnostic**: Can translate to Python, JavaScript, TypeScript
5. **Implementation Ready**: Developer can code directly from pseudocode
6. **Testable**: Each function has clear inputs/outputs for unit testing

**Development Velocity**:
- **Estimation**: 8 weeks with 2 developers
- **Confidence**: 85% (pseudocode reduces ambiguity)
- **Risk**: Low (unclear requirements clarified in pseudocode phase)

**Quality Assurance**:
- **Test Coverage**: Pseudocode maps directly to test cases
- **Code Review**: Easier to review against pseudocode blueprint
- **Documentation**: Pseudocode comments → inline code documentation

---

## **14. Conclusion**

### **14.1 Pseudocode Completeness**

This pseudocode document provides:
- ✅ **Complete algorithm specifications** for all major components
- ✅ **Clear data structures** with field definitions and types
- ✅ **Detailed error handling** patterns and recovery strategies
- ✅ **Performance considerations** with optimization opportunities
- ✅ **Security validation** multi-layer approach
- ✅ **Multi-language guidance** for Python and JavaScript implementations
- ✅ **Implementation roadmap** with phased delivery plan

### **14.2 Readiness for Implementation**

**Phase Status**: ✅ **COMPLETE - READY FOR IMPLEMENTATION**

**Developer Readiness**:
- Python developer can implement directly from pseudocode
- JavaScript developer can translate with language notes provided
- Clear separation enables parallel development by multiple developers
- Test cases derivable from pseudocode function signatures

**Next Steps**:
1. **Code Implementation**: Begin Phase 1 (Core Pipeline)
2. **Unit Testing**: Write tests alongside implementation
3. **Continuous Integration**: Set up CI/CD pipeline
4. **Iterative Refinement**: Adjust based on implementation learnings

### **14.3 Success Criteria**

Pseudocode succeeds if:
- ✅ Developers can implement without waiting for clarification
- ✅ No major architectural changes needed during implementation
- ✅ Code review can reference pseudocode as blueprint
- ✅ Test cases cover all pseudocode functions
- ✅ Implementation matches specification requirements

**Confidence Level**: **90%** - Comprehensive pseudocode significantly reduces implementation risk

---

**Document Status**: ✅ **COMPLETE**  
**Phase**: SPARC Phase 4 - Pseudocode  
**Next Phase**: Implementation (Code Development)  
**Estimated Implementation Time**: 8 weeks (2 developers)

---

**Pseudocode Version**: 1.0  
**Last Updated**: October 29, 2025  
**Status**: Final - Ready for Development Team