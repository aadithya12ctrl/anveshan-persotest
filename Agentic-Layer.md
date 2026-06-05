# Untitled

# **Agentic Layer - File Structure & Implementation Plan**

## **File Structure**

```
text
agentic-layer/
├── README.md
├── requirements.txt
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── llm_config.py
│   ├── privacy_config.py
│   └── monitoring_thresholds.py
│
├── core/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── base_agent.py
│   └── exceptions.py
│
├── agents/
│   ├── __init__.py
│   ├── assessment/
│   │   ├── __init__.py
│   │   ├── question_generator.py
│   │   ├── trait_scorer.py
│   │   └── scorecard_generator.py
│   │
│   └── monitoring/
│       ├── __init__.py
│       ├── proactive_worker.py
│       └── intervention_generator.py
│
├── rag/
│   ├── __init__.py
│   ├── context_manager.py
│   ├── embeddings.py
│   ├── personality_state.py
│   └── session_history.py
│
├── llm/
│   ├── __init__.py
│   ├── llama_interface.py
│   ├── prompt_templates.py
│   └── reflection_loop.py
│
├── privacy/
│   ├── __init__.py
│   ├── pii_scrubber.py
│   ├── pii_detector.py
│   └── rehydrator.py
│
├── data/
│   ├── __init__.py
│   ├── models.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_profile_repo.py
│   │   ├── session_repo.py
│   │   └── screentime_repo.py
│   │
│   └── schemas/
│       ├── __init__.py
│       ├── user_profile.py
│       ├── screentime.py
│       ├── assessment.py
│       └── intervention.py
│
├── screentime/
│   ├── __init__.py
│   ├── collector.py
│   ├── analyzer.py
│   ├── baseline_calculator.py
│   └── threshold_detector.py
│
├── observability/
│   ├── __init__.py
│   ├── trace_logger.py
│   ├── metrics.py
│   └── evaluations.py
│
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── assessment.py
│   │   ├── monitoring.py
│   │   └── reports.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── logging.py
│   │
│   └── dependencies.py
│
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   ├── formatters.py
│   └── helpers.py
│
└── tests/
    ├── __init__.py
    ├── unit/
    │   ├── test_orchestrator.py
    │   ├── test_agents/
    │   ├── test_privacy/
    │   └── test_rag/
    │
    ├── integration/
    │   ├── test_assessment_flow.py
    │   ├── test_monitoring_flow.py
    │   └── test_end_to_end.py
    │
    └── fixtures/
        ├── sample_screentime.py
        └── sample_profiles.py
```

---

## **Implementation Plan**

### **Phase 1: Foundation & Core Infrastructure**

### **1.1 Configuration & Settings**

- **Purpose**: Centralize all configuration management
- **Components**:
    - Settings management for different environments (dev, staging, production)
    - LLM configuration including model selection, temperature, max tokens
    - Privacy configuration for PII detection rules and DPDP compliance
    - Monitoring thresholds for different user segments and apps
- **Dependencies**: None
- **Outputs**: Configuration objects accessible throughout application

### **1.2 Data Layer Setup**

- **Purpose**: Establish data models and persistence layer
- **Components**:
    - Define schema models for user profiles, trait scores, screentime data
    - Create session history schema with conversation tracking
    - Define assessment response schema with metadata
    - Build intervention log schema
    - Implement repository pattern for data access
- **Dependencies**: Database selection and setup
- **Outputs**: Clean data access layer with type-safe schemas

### **1.3 Base Agent Architecture**

- **Purpose**: Create reusable agent framework
- **Components**:
    - Abstract base agent class with common lifecycle methods
    - Standard interfaces for agent communication
    - Error handling and retry logic
    - Agent state management
    - Logging integration points
- **Dependencies**: Configuration layer
- **Outputs**: Base classes for all specialized agents

---

### **Phase 2: Privacy & Security Layer**

### **2.1 PII Detection & Scrubbing**

- **Purpose**: Ensure DPDP compliance before LLM processing
- **Components**:
    - Build PII detector using regex, NER models, and custom rules
    - Implement entity extraction for names, phone numbers, emails, addresses
    - Create tokenization system for detected PII
    - Build scrubber that replaces PII with placeholder tokens
    - Add support for Indian-specific PII patterns (Aadhaar, PAN, etc.)
- **Dependencies**: None (can use lightweight NER models)
- **Outputs**: Clean prompts with PII removed, token mapping stored

### **2.2 Rehydration System**

- **Purpose**: Restore PII after LLM processing where contextually appropriate
- **Components**:
    - Build token-to-entity mapping store (in-memory with expiry)
    - Implement rehydration logic that replaces tokens with original PII
    - Add selective rehydration (only restore where needed)
    - Include audit logging of what was rehydrated and why
- **Dependencies**: PII Scrubber
- **Outputs**: Contextually complete responses with appropriate PII restored

---

### **Phase 3: LLM Integration & Reflection**

### **3.1 Llama 3 Interface**

- **Purpose**: Abstract LLM interaction with self-hosted Llama 3
- **Components**:
    - Build connection manager for Llama 3 API/endpoint
    - Implement prompt formatting and tokenization
    - Add retry logic with exponential backoff
    - Create response parsing and validation
    - Implement rate limiting and quota management
    - Add fallback mechanisms for model unavailability
- **Dependencies**: Llama 3 deployment
- **Outputs**: Reliable LLM interface with error handling

### **3.2 Prompt Template System**

- **Purpose**: Manage and version all prompts
- **Components**:
    - Create template registry for different prompt types
    - Build dynamic prompt assembly from context variables
    - Implement few-shot example management
    - Add prompt versioning and A/B testing support
    - Include templates for: question generation, trait scoring, interventions, reflections
- **Dependencies**: LLM interface
- **Outputs**: Centralized, testable prompt management

### **3.3 Reflection Loop**

- **Purpose**: Validate LLM outputs before downstream processing
- **Components**:
    - Implement confidence scoring mechanism
    - Build validation rules for different output types
    - Create re-prompting strategy with iteration limits
    - Add quality metrics extraction (coherence, relevance, safety)
    - Implement circuit breaker after N failed attempts
    - Log all reflection decisions for analysis
- **Dependencies**: LLM interface, Prompt templates
- **Outputs**: High-quality, validated LLM responses

---

### **Phase 4: RAG & Context Management**

### **4.1 Embeddings System**

- **Purpose**: Enable semantic search over personality and historical data
- **Components**:
    - Set up embedding model (sentence-transformers or similar)
    - Build embedding pipeline for user responses, traits, patterns
    - Implement vector storage (using FAISS, Pinecone, or similar)
    - Create similarity search functionality
    - Add batch embedding for efficiency
- **Dependencies**: Embedding model selection
- **Outputs**: Semantic search capability over user data

### **4.2 Personality State Manager**

- **Purpose**: Maintain live user personality profile
- **Components**:
    - Build trait score storage with Big Five dimensions
    - Implement procrastination/productivity profile structure
    - Create profile update mechanisms (incremental scoring)
    - Add profile versioning to track changes over time
    - Implement profile retrieval optimized for agent access
- **Dependencies**: Data layer
- **Outputs**: Fast, queryable personality profiles

### **4.3 Session History Manager**

- **Purpose**: Track conversation context and user interactions
- **Components**:
    - Build conversation buffer with sliding window
    - Implement session state persistence
    - Create context summarization for long conversations
    - Add retrieval of relevant past interactions
    - Implement session cleanup and archival
- **Dependencies**: Data layer, Embeddings
- **Outputs**: Contextual conversation memory

### **4.4 Context Manager Integration**

- **Purpose**: Orchestrate all RAG components
- **Components**:
    - Build unified context retrieval interface
    - Implement context ranking and selection
    - Create context window management (token budgets)
    - Add context freshness tracking
    - Implement context caching for performance
- **Dependencies**: All RAG components
- **Outputs**: Smart context injection for agents

---

### **Phase 5: Screentime Integration**

### **5.1 Screentime Data Collection**

- **Purpose**: Ingest screentime data from various sources
- **Components**:
    - Define standardized screentime data schema
    - Build adapters for different data sources (iOS Screen Time, Android Digital Wellbeing, third-party apps)
    - Implement data validation and sanitization
    - Create periodic sync mechanisms
    - Add app categorization (social media, productivity, entertainment)
- **Dependencies**: Data layer
- **Outputs**: Normalized screentime data store

### **5.2 Screentime Analyzer**

- **Purpose**: Extract behavioral patterns from screentime
- **Components**:
    - Implement pattern detection (peak usage times, app preferences)
    - Build metrics calculation (total time, session count, context switches)
    - Create temporal analysis (daily/weekly trends)
    - Add distraction event detection
    - Implement app usage correlation analysis
- **Dependencies**: Screentime collector
- **Outputs**: Behavioral insights from screentime

### **5.3 Baseline Calculator**

- **Purpose**: Establish user-specific normal behavior
- **Components**:
    - Implement statistical baseline calculation (median, percentiles)
    - Build adaptive baseline that evolves with user behavior
    - Create per-app and per-category baselines
    - Add time-of-day and day-of-week segmentation
    - Implement baseline refresh mechanisms
- **Dependencies**: Screentime analyzer
- **Outputs**: Personalized behavioral baselines

### **5.4 Threshold Detector**

- **Purpose**: Identify when current usage exceeds baseline
- **Components**:
    - Implement threshold breach detection logic
    - Build severity classification (minor, moderate, severe)
    - Create cooldown periods to avoid alert fatigue
    - Add contextual threshold adjustment (work hours vs leisure)
    - Implement trend-based early warning
- **Dependencies**: Baseline calculator
- **Outputs**: Real-time breach events for intervention

---

### **Phase 6: Assessment Phase Agents**

### **6.1 Orchestrator**

- **Purpose**: Route requests and coordinate agent execution
- **Components**:
    - Build request routing logic for different endpoints
    - Implement agent selection and sequencing
    - Create execution plan generation
    - Add error recovery and fallback routing
    - Implement result aggregation from multiple agents
    - Build phase transition logic (assessment → monitoring)
- **Dependencies**: Base agent, all specialized agents
- **Outputs**: Coordinated multi-agent workflows

### **6.2 Question Generation Agent**

- **Purpose**: Generate adaptive personality assessment questions
- **Components**:
    - Build Big Five trait targeting logic
    - Implement adaptive questioning (follow-ups based on responses)
    - Create question templates for each dimension
    - Add variety mechanisms to avoid repetition
    - Implement question difficulty calibration
    - Build conversational question framing (not clinical)
    - Add stop condition detection (sufficient coverage)
- **Dependencies**: LLM interface, Reflection loop, RAG
- **Outputs**: Contextual, trait-targeted questions

### **6.3 Trait Scoring Agent**

- **Purpose**: Combine user responses with screentime to build profile
- **Components**:
    - Implement response parsing and extraction
    - Build trait inference from conversational responses
    - Create screentime signal integration (behavioral validation)
    - Implement scoring algorithms for Big Five dimensions
    - Build procrastination/productivity scoring
    - Add confidence intervals for scores
    - Create profile assembly and validation
    - Implement profile persistence
- **Dependencies**: LLM interface, Screentime analyzer, Data layer
- **Outputs**: Complete user trait profiles

### **6.4 Scorecard Generator**

- **Purpose**: Translate trait profile into user-friendly report
- **Components**:
    - Build score visualization formatting
    - Implement pattern narrative generation
    - Create actionable solution recommendations
    - Add personalized insight generation using LLM
    - Implement report template system
    - Build multi-format output (JSON, HTML, PDF)
    - Add tone adjustment (encouraging, not judgmental)
- **Dependencies**: Trait profiles, LLM interface
- **Outputs**: User-facing scorecard reports

---

### **Phase 7: Monitoring Phase Agents**

### **7.1 Proactive Agent Worker**

- **Purpose**: Continuously monitor screentime against baseline
- **Components**:
    - Build real-time screentime stream processor
    - Implement baseline comparison logic
    - Create threshold breach detection integration
    - Add event filtering to reduce noise
    - Implement priority queue for interventions
    - Build monitoring state management (active/paused)
    - Add user-specific monitoring rules
- **Dependencies**: Screentime system, User profiles
- **Outputs**: Intervention trigger events

### **7.2 Intervention Generator**

- **Purpose**: Create personalized nudges for threshold breaches
- **Components**:
    - Build context assembly (breach severity + trait profile + current activity)
    - Implement intervention tone personalization based on traits
    - Create intervention variety to avoid habituation
    - Add timing optimization (when to send)
    - Implement intervention templates (gentle nudge, strong redirect, etc.)
    - Build intervention effectiveness tracking
    - Add cooldown and rate limiting
- **Dependencies**: LLM interface, User profiles, PII scrubber
- **Outputs**: Personalized push notifications

---

### **Phase 8: Observability & Monitoring**

### **8.1 Trace Logger**

- **Purpose**: Create comprehensive audit trail
- **Components**:
    - Build structured logging system with trace IDs
    - Implement step-level logging for all agent actions
    - Create failure flag detection and alerting
    - Add log aggregation and search
    - Implement log retention and archival
    - Build privacy-safe logging (no PII in logs)
- **Dependencies**: All components
- **Outputs**: Searchable audit logs

### **8.2 Metrics System**

- **Purpose**: Track system performance and quality
- **Components**:
    - Define key metrics (latency, success rate, user engagement)
    - Build metric collection points in agents
    - Implement metric aggregation and rollup
    - Create dashboard integration
    - Add alerting for metric anomalies
    - Build A/B test metric tracking
- **Dependencies**: Trace logger
- **Outputs**: Real-time performance dashboards

### **8.3 Evaluation Pipeline**

- **Purpose**: Offline quality assessment
- **Components**:
    - Build evaluation dataset curation from logs
    - Implement quality scoring for LLM outputs
    - Create trait scoring accuracy evaluation
    - Add intervention effectiveness evaluation
    - Implement automated regression testing
    - Build human evaluation interfaces
- **Dependencies**: Trace logger, Metrics
- **Outputs**: Quality scores and improvement insights

---

### **Phase 9: API Layer**

### **9.1 Chat Endpoints**

- **Purpose**: Handle real-time user conversations
- **Components**:
    - Build WebSocket or Server-Sent Events for streaming
    - Implement REST endpoints for message sending
    - Create session management (create, resume, close)
    - Add typing indicators and status updates
    - Implement message history retrieval
- **Dependencies**: Orchestrator
- **Outputs**: Chat API

### **9.2 Assessment Endpoints**

- **Purpose**: Manage assessment lifecycle
- **Components**:
    - Build assessment start endpoint
    - Implement progress tracking endpoint
    - Create assessment completion endpoint
    - Add scorecard retrieval endpoint
    - Implement assessment restart/reset logic
- **Dependencies**: Assessment agents
- **Outputs**: Assessment management API

### **9.3 Monitoring Endpoints**

- **Purpose**: Control monitoring behavior
- **Components**:
    - Build monitoring activation endpoint
    - Implement pause/resume monitoring
    - Create intervention history retrieval
    - Add monitoring settings update
    - Implement baseline recalculation trigger
- **Dependencies**: Monitoring agents
- **Outputs**: Monitoring control API

### **9.4 Reports Endpoints**

- **Purpose**: Provide analytics and insights
- **Components**:
    - Build scorecard retrieval endpoint
    - Implement trend reports (weekly, monthly)
    - Create progress tracking endpoint
    - Add export functionality
    - Implement scheduled report generation
- **Dependencies**: Scorecard generator, Data layer
- **Outputs**: Reporting API

---

### **Phase 10: Testing & Validation**

### **10.1 Unit Tests**

- **Purpose**: Validate individual components
- **Components**:
    - Write tests for all agents with mocked dependencies
    - Test privacy layer with known PII samples
    - Test RAG retrieval accuracy
    - Test screentime analysis logic
    - Test orchestrator routing decisions
- **Dependencies**: All components
- **Outputs**: High unit test coverage

### **10.2 Integration Tests**

- **Purpose**: Validate multi-component workflows
- **Components**:
    - Test complete assessment flow end-to-end
    - Test monitoring and intervention flow
    - Test PII scrubbing and rehydration round-trip
    - Test LLM reflection loop behavior
    - Test data persistence and retrieval
- **Dependencies**: Test environment setup
- **Outputs**: Validated integration paths

### **10.3 End-to-End Tests**

- **Purpose**: Validate full user journeys
- **Components**:
    - Test new user onboarding through scorecard
    - Test ongoing monitoring with simulated screentime
    - Test profile evolution over time
    - Test error handling and recovery
    - Test concurrent user scenarios
- **Dependencies**: Staging environment
- **Outputs**: Production-ready system validation

---

## **Cross-Cutting Concerns**

### **Error Handling Strategy**

- Implement graceful degradation at each layer
- Build retry logic with exponential backoff
- Add circuit breakers for external dependencies
- Create user-friendly error messages
- Log all errors with context for debugging

### **Performance Optimization**

- Implement caching at RAG, LLM, and data layers
- Add batch processing where applicable
- Use async/await for I/O-bound operations
- Implement connection pooling
- Add lazy loading for heavy resources

### **Security Measures**

- Implement authentication and authorization
- Add rate limiting per user and endpoint
- Encrypt data at rest and in transit
- Implement secure token storage for PII mapping
- Add input validation and sanitization
- Implement CORS and security headers

### **Scalability Considerations**

- Design stateless agents where possible
- Implement horizontal scaling for agent workers
- Add message queue for async processing
- Use distributed caching (Redis)
- Implement database read replicas
- Add load balancing