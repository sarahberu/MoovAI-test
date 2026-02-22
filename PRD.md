# AI Market Analysis Agent – Fitness Ring (Canada Market)

---

## 1. Purpose of This Assignment

This project aims to demonstrate the design and implementation of an AI agent capable of orchestrating multiple analytical tools to generate a structured market intelligence report.

The primary objective is not tool sophistication, but:

- Agent orchestration  
- Modular architecture  
- Clean separation of responsibilities  
- Effective LLM integration  
- Testability and maintainability  

The system analyzes the **Canadian market for a premium fitness ring product**.

---

## 2. Product Context

### Target Product Example

**Oura Ring Gen 3**  
Market: Canada  

### Geographic Focus: Canada

The system simulates:

- Canadian pricing in CAD  
- Canadian retailers (Amazon.ca, BestBuy.ca, Official Store)  
- Canadian/North American consumer sentiment  

This defined geographic scope:

- Adds realism  
- Allows currency normalization  
- Keeps data simulation coherent  
- Demonstrates regional market awareness  

---

## 3. Architectural Approach

### Chosen Approach: Native Python Orchestration

The solution implements a custom orchestration layer in Python rather than using a framework such as LangGraph or CrewAI.

#### Justification

1. Demonstrates explicit understanding of agent execution flow  
2. Provides full control over tool sequencing  
3. Enables deterministic testing  
4. Reduces abstraction complexity  
5. Highlights architectural clarity within the 4–6 hour constraint  

The design prioritizes transparency and modularity over framework usage.

---

## 4. System Overview

### High-Level Flow

```
Client Request  
→ REST API (FastAPI)  
→ Orchestrator  
→ Web Scraper Tool  
→ Sentiment Analyzer Tool  
→ Report Generator Tool  
→ Structured JSON Response
```

Each tool:

- Implements a clear interface  
- Returns structured output  
- Is independently testable  
- Can be replaced without impacting other components  

---

## 5. Functional Scope (Steps 1–3 Implementation)

The implemented system includes:

- REST API endpoint  
- Main orchestration agent  
- 3 analytical tools  
- LLM-based structured report generation  
- Unit tests  
- Docker containerization  

### Out of scope (conceptual only)

- Real scraping infrastructure  
- Database persistence  
- Monitoring system  
- Horizontal scaling implementation  

---

## 6. Tools Design

### 6.1 Web Scraper Tool (Mocked)

**Purpose**  
Simulate collection of product and competitor data from Canadian e-commerce platforms.

Simulated data includes:

- Prices in CAD from:
  - Amazon.ca  
  - BestBuy.ca  
  - Official Store  
- Competitor products in Canada  
- Product specifications  
- Customer review samples  

**Example Output Structure**

- `prices_by_retailer`  
- `average_price`  
- `competitors`  
- `specifications`  
- `review_samples`  

**Design Principle**

The scraper is abstracted behind an interface.  
In production, this module could be replaced with:

- A real scraping service  
- A third-party product API  
- A data provider integration  

This demonstrates decoupling and production awareness.

---

### 6.2 Sentiment Analyzer Tool (LLM-Based)

**Purpose**  
Analyze customer reviews and extract structured insights.

Responsibilities:

- Determine overall sentiment  
- Extract recurring strengths  
- Extract recurring weaknesses  
- Identify perceived value positioning (budget, mid-range, premium)  

**Implementation Strategy**

- LLM prompt with structured output requirements  
- Deterministic format (JSON schema)  
- Controlled temperature for stability  

This tool demonstrates:

- Prompt engineering  
- Structured LLM output control  
- Context management  
- Clean integration into agent pipeline  

---

### 6.3 Report Generator Tool (LLM-Based)

**Purpose**  
Transform aggregated analytical data into a strategic business report.

**Inputs**

- Pricing data  
- Competitor landscape  
- Sentiment insights  

**Output**

Structured JSON report containing:

- Executive summary  
- Pricing analysis  
- Competitive positioning  
- Customer perception analysis  
- Strategic recommendations for the Canadian market  

**Design Considerations**

- LLM role defined as “Market Intelligence Analyst”  
- Structured output instructions  
- Deterministic formatting constraints  
- No raw unfiltered data passed unnecessarily  

This tool demonstrates higher-level reasoning orchestration.

---

## 7. Orchestrator Design

The orchestrator is the core component of the system.

Responsibilities:

1. Receive validated API request  
2. Execute Web Scraper  
3. Pass reviews to Sentiment Analyzer  
4. Aggregate pricing and sentiment data  
5. Send structured data to Report Generator  
6. Return final structured report  
7. Handle tool-level exceptions gracefully  

### Design Principles

- Explicit sequential execution  
- Clear data contracts  
- Strong separation of concerns  
- Centralized error handling  
- Logging at each execution stage  

### Future-ready

The architecture can later support:

- Parallel tool execution  
- Caching layer  
- Persistent storage  
- Tool retries  

---

## 8. API Design

### Endpoint

```
POST /analyze
```

### Request Body

- `product_name`  
- `market` (must be Canada)  

### Response Structure

- `executive_summary`  
- `pricing_analysis`  
- `competitive_landscape`  
- `sentiment_analysis`  
- `strategic_recommendations`  

All outputs are structured JSON.

---

## 9. LLM Integration Strategy

LLM is used for:

- Sentiment analysis  
- Strategic report generation  

### Integration principles

- Clear role definition  
- Structured JSON output  
- Controlled token usage  
- Deterministic behavior  
- Validation of LLM responses before returning to client  

This demonstrates responsible LLM integration.

---

## 10. Non-Functional Requirements

- Modular codebase  
- Deterministic unit tests  
- Replaceable tool interfaces  
- Clear error propagation  
- Dockerized environment  
- Python 3.13 compatibility  

---

## 11. Testing Strategy

Tests cover:

- Web Scraper output structure  
- Sentiment Analyzer schema validation  
- Orchestrator execution flow  
- Tool failure scenarios  
- Final report structure validation  

All external dependencies mocked for deterministic results.

---

## 12. Design Philosophy

This solution prioritizes:

- Agent orchestration clarity  
- Explicit execution flow  
- Structured LLM usage  
- Extensibility  
- Production-aware design  
- Time-efficient implementation  

The goal is to demonstrate architectural maturity rather than overengineering individual tools.