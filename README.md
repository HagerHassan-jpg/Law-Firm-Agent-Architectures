# Ashford & Kane LLP — Legal Case Intake Evaluation System

This repository contains the full implementation of an **Automated Legal Case Intake System** for **Ashford & Kane LLP**, evaluated across four distinct agent architectures as part of the Agent Design Lab.

---

## 🏢 Company & Problem Definition

* **Company:** Ashford & Kane LLP (Law Firm)
* **Problem:** **Case Intake Evaluation & Urgency Triage**
  * The firm receives high volumes of legal inquiries and case documents daily.
  * The intake system must evaluate case eligibility based on:
    1. **Document Completeness & Deadlines** (Court urgency vs missing files)
    2. **Conflict of Interest** (Confirmed or suspected conflicts)
    3. **Specialist Availability** (Exact vs related legal specialists)
    4. **Client History & Archival Records**

### Why an Agent is Needed instead of a Simple Script
Legal case evaluation requires multi-step conditional reasoning. The next evaluation step depends entirely on the outcome of the previous step (e.g., checking archival history only if secondary documents are missing, or triggering immediate escalation if a conflict of interest is detected). A static script lacks the contextual adaptability to handle edge cases and dynamic tool usage.

---

## 🏗️ The Four Architectures

1. `reactive/` — **Reactive (Rule-Based) Agent:** Pure `if/else` keyword matching logic without model calls.
2. `unconstrained_react/` — **Unconstrained ReAct Agent:** Free-form ReAct loop utilizing Gemini Native Function Calling without schema constraints or step limits.
3. `routing/` — **Deterministic Routing Agent:** Single LLM call classifying case attributes, followed by deterministic execution functions.
4. `constrained_react/` — **Constrained ReAct Agent:** Schema-validated reasoning loop using Pydantic, strict `ALLOW_LIST` enforcement, and `MAX_STEPS = 5` limit with fallback escalation.

---

## 📊 Comparison Table

| Architecture | Calls / Request | Latency | Cost / Tokens | Failure / Edge Case Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **1. Reactive (Rule-Based)** | 0 | $< 5\text{ms}$ | $\$0.00$ | Fails completely if keywords or exact status flags are phrased differently or missing. |
| **2. Unconstrained ReAct** | 3 – 6 Calls | $4.0 - 8.0\text{s}$ | High | Prone to extra tool calls, higher latency, and potential infinite reasoning loops on ambiguous cases. |
| **3. Deterministic Routing** | 1 Call | $\sim 1.2\text{s}$ | Very Low | Fast and predictable, but unable to dynamically investigate secondary evidence or query client history iteratively. |
| **4. Constrained ReAct** | 2 – 4 Calls | $2.0 - 3.5\text{s}$ | Moderate | Highly reliable. Strictly adheres to output schema, respects tool allow-lists, and automatically escalates when `MAX_STEPS = 5` is reached. |

---

