## Constrained ReAct Agent

Model: Groq (llama-3.3-70b-versatile)

### How to run
1. pip install -r requirements.txt
2. Copy .env.example to .env and add your GROQ_API_KEY
3. python main.py

Constraints:
- Schema: see schemas.py (AgentStep)
- Tool allow-list: see tools.py (ALLOWED_TOOLS)
- MAX_STEPS: see config.py