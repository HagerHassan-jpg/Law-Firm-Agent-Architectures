# ⚖️ Unconstrained ReAct Agent

An AI-powered legal case intake evaluation system built using the **ReAct Agent Architecture** and **Google Gemini API**.

The agent is capable of reasoning step-by-step, deciding which tools to use, and producing a final legal intake decision based on the available case information.

---

# 📌 Overview

This project simulates the **Case Intake Evaluation** process inside a law firm.

Instead of following a fixed workflow, the agent can freely decide:

- Which tool to call
- When to call it
- Whether to call one or multiple tools
- When enough information has been collected

After reasoning over the available evidence, the agent returns a structured JSON decision.

---

# 📂 Project Structure

```
unconstrained_react/
│
├── agent.py
├── main.py
├── models.py
├── prompts.py
├── tools.py
├── requirements.txt
└── README.md
```

---

# 🛠 Available Tools

The agent has access to the following tools:

- 📄 Document Evaluation
- ⚖️ Conflict of Interest Evaluation
- 👨‍⚖️ Specialist Availability Evaluation
- 📁 Client History Evaluation

Unlike constrained agents, **there is no predefined order** for using these tools.

---

# ✅ Possible Decisions

The agent must return **exactly one** of the following decisions:

- Accept Case
- Provisionally Accept and Request Missing Documents
- Request More Information
- Reject Due to Conflict of Interest
- Escalate for Senior Review
- Escalate Due to No Available Specialist

---

# 🤖 Agent Workflow

1. Receive case information.
2. Analyze the case.
3. Decide which tool(s) to call.
4. Collect the returned information.
5. Continue reasoning if needed.
6. Produce the final JSON decision.

---

# 📦 Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project directory.

Example:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# ▶️ Run the Project

```bash
python main.py
```

Enter a Case ID when prompted.

Example:

```
Enter Case ID:
CASE-001
```

---

# 📤 Example Output

```json
{
  "decision": "Accept Case",
  "flags": [],
  "reasoning": "All required checks passed successfully."
}
```

---

# 🧠 Technologies Used

- Python
- Google Gemini API
- ReAct Agent Architecture
- Function Calling
- JSON

---

# 👩‍💻 Author

Case Intake Evaluation Project

Faculty AI Agent Architectures Assignment
