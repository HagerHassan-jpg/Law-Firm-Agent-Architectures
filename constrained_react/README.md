# Constrained ReAct Agent

This folder contains the implementation of the **Constrained ReAct Agent** for the legal case intake evaluation system at **Ashford & Kane LLP**.

Unlike unconstrained implementations, this agent operates within strict runtime guardrails to ensure predictable, reliable, and secure execution during legal triage.

---

## 🏗️ Technical Architecture & Key Features

1. **Strict Output Schema Validation (`schemas.py`):**
   * Uses **Pydantic** (`AgentActionStep`) with `response_schema` in the Gemini API.
   * Guarantees that every model response strictly follows a pre-defined JSON structure, eliminating JSON parsing failures and hallucinations.

2. **Explicit Tool Allow-List (`agent.py`):**
   * Enforces a hardcoded registry (`ALLOWED_TOOLS`).
   * The agent can strictly only invoke approved functions (`evaluate_documents`, `evaluate_conflict`, `evaluate_specialist`, `evaluate_client_history`). Any unauthorized tool call is caught and rejected immediately.

3. **Execution Cap (`MAX_STEPS = 5`):**
   * Prevents infinite reasoning loops and runaway API costs.
   * If the agent reaches 5 execution steps without concluding a decision, the system automatically halts execution and triggers a fallback **Escalation**.

4. **Automated Escalation Mechanism:**
   * Triggers an explicit `ESCALATED` status whenever:
     * High conflict/legal risks are identified.
     * The `MAX_STEPS` limit is reached without a definitive answer.
     * Unresolvable ambiguities occur during tool evaluation.

5. **API Resilience & Retries:**
   * Integrated with `tenacity` retry logic to gracefully handle network issues or transient API errors.

---

## 📁 File Structure

```text
constrained_react/
├── schemas.py      # Pydantic schemas enforcing output structure
├── agent.py        # Constrained ReAct loop, allow-list logic, and main execution
└── README.md       # Documentation for the constrained agent module
