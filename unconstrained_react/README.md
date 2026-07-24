# Unconstrained ReAct Agent

## Overview

This project implements an Unconstrained ReAct Agent for a law firm's case intake evaluation process.

The agent uses the Google Gemini API to analyze legal cases and decide which tools to use before making a final decision. Unlike constrained agents, there is no predefined order for calling tools. The agent selects the necessary tools dynamically based on the case information.

---

## Project Structure

```
unconstrained_react/
│
├── agent.py
├── main.py
├── models.py
├── prompts.py
├── tools.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Available Tools

The agent can use the following tools during evaluation:

- Document Evaluation
- Conflict of Interest Evaluation
- Specialist Availability Evaluation
- Client History Evaluation

The agent may use one tool, multiple tools, or skip unnecessary tools depending on the case.

---

## Possible Decisions

The final decision will always be one of the following:

- Accept Case
- Provisionally Accept and Request Missing Documents
- Request More Information
- Reject Due to Conflict of Interest
- Escalate for Senior Review
- Escalate Due to No Available Specialist

---

## Requirements

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file and add your Gemini API key:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

An example is provided in `.env.example`.

---

## Running the Project

Run the project using:

```bash
python main.py
```

Enter a valid Case ID when prompted. The agent will evaluate the case and return the final decision as a JSON object.

---

## Example Output

```json
{
    "decision": "Accept Case",
    "flags": [],
    "reasoning": "All required checks passed successfully."
}
```

---

## Technologies Used

- Python
- Google Gemini API
- ReAct Agent Architecture
- Function Calling
- JSON
