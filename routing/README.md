# Routing Agent

## Overview

This Routing Agent uses Gemini to analyze a legal case and classify it according to the company's business rules. The LLM only performs the analysis, while the final business decision is made using deterministic Python rules.

The agent evaluates four categories:

- Documents
- Conflict of Interest
- Specialist Availability
- Client History

Based on the analysis, the application returns one of the following decisions:

- Accept Case
- Reject Due to Conflict of Interest
- Request More Information
- Provisionally Accept and Request Missing Documents
- Assign to Related Specialist
- Escalate for Senior Review
- Escalate Due to No Available Specialist

---

## Model / Provider

- **Provider:** Google Gemini
- **Model:** `gemini-flash-latest`

---

## Project Structure

```
routing/
│
├── routing_agent.py
├── README.md
└── .env
```

---

## Run

From the project root:

```bash
python routing/routing_agent.py
```

The program will:

1. Load a test legal case.
2. Send it to Gemini for analysis.
3. Receive the structured JSON output.
4. Apply the business rules.
5. Print the final decision.

---

## Output Example

```json
{
  "documents": "missing_secondary_urgent",
  "conflict": "none",
  "specialist": "assign_related",
  "client_history": "reuse_document"
}
```

Final Decision:

```
Provisionally Accept and Request Missing Documents
```