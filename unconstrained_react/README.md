# Unconstrained ReAct Agent — Case Intake Evaluation

## What it does
Evaluates incoming legal cases and decides one of six outcomes:
Accept Case, Provisionally Accept and Request Missing Documents, 
Request More Information, Reject Due to Conflict of Interest, 
Escalate for Senior Review, or Escalate Due to No Available Specialist.

The model freely decides which tools to call, in what order, and when 
it has enough information to make a final decision — there is no fixed 
schema, no tool allow-list, and no step limit.

## Model / Provider
Runs on **Groq** (`llama-3.3-70b-versatile`).

> Note: this was originally built on Google Gemini (`gemini-2.5-flash`), 
> but was switched to Groq after Gemini's models became unavailable to 
> new API users and the newer Gemini 3 preview models returned persistent 
> `503 UNAVAILABLE` errors during testing.

## How to run

1. Install dependencies:
      pip install -r requirements.txt 
2. Create a `.env` file in this folder with:

     GROQ_API_KEY=your_key_here

   (Get a free key at https://console.groq.com)

3. Run:

python main.py


4. Enter a Case ID when prompted (see `shared/test_cases.json` for 
   available test cases, e.g. `CASE-001`).

## Files
- `main.py` — entry point, loads the case and runs the agent
- `agent.py` — the ReAct loop and Groq client setup
- `prompts.py` — system prompt defining the agent's role and decision options
- `models.py` — dataclass describing the case structure
## How to run

1. Install dependencies:
