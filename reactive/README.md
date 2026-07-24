# Reactive Agent

## Overview

This Reactive Agent evaluates legal cases using predefined business rules. It processes the case information in a fixed order and returns a decision without using any language model or reasoning capabilities.

The agent checks:

- Conflict of Interest
- Document Status
- Specialist Availability
- Client History (Archived Documents)

Possible decisions include:

- Accept Case
- Reject Due to Conflict of Interest
- Request More Information
- Provisionally Accept and Request Missing Documents
- Escalate for Senior Review
- Escalate Due to No Available Specialist

---

## Project Structure

```
reactive/
│
├── reactive_agent.py
└── README.md
```


---

## Run

From the project root:

```bash
python reactive/reactive_agent.py
```

The program will:

1. Load a sample legal case.
2. Evaluate it using predefined business rules.
3. Print the decision, triggered flags, and reasoning.

---
