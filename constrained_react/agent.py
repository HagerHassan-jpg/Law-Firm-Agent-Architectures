import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError
from tenacity import retry, stop_after_attempt, wait_fixed

from config import MAX_STEPS, MODEL_NAME
from schemas import AgentStep
from tools import ALLOWED_TOOLS, load_case

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a legal case intake agent at Ashford & Kane LLP.
You must decide what to do with a case using ONLY the tools listed below,
following the firm's business rules in priority order.

Business rules priority:
1. Confirmed Conflict of Interest -> Reject the case.
2. Suspected Conflict + Weak Evidence -> Reject or Escalate for Senior Review.
3. Missing Critical Documents -> Request More Information.
4. Missing Secondary Documents + Urgent Deadline (<=7 days) -> Provisionally Accept and Request Missing Documents.
5. No Exact Specialist + Related Specialist Available + Urgent Deadline (<=3 days) -> Assign to related specialist (Accept Case).
6. No Suitable Specialist -> Escalate Due to No Available Specialist.
7. Otherwise -> Accept Case.

Available tools:
- evaluate_documents
- evaluate_conflict
- evaluate_specialist
- evaluate_client_history

You must respond ONLY in this JSON format, nothing else:
{
  "thought": "short reasoning",
  "action": "one of: evaluate_documents, evaluate_conflict, evaluate_specialist, evaluate_client_history, final_answer, escalate",
  "action_input": {"case_id": "CASE-001"},
  "final_decision": "only fill this when action is final_answer or escalate"
}
"""


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def call_model(messages):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def run_agent(case_id: str):
    case = load_case(case_id)
    if case is None:
        return {"error": "Case not found"}

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Evaluate this case: {json.dumps(case)}"},
    ]

    steps_taken = 0

    while steps_taken < MAX_STEPS:
        raw = call_model(messages)

        try:
            step = AgentStep.model_validate_json(raw)
        except ValidationError as e:
            messages.append({"role": "assistant", "content": raw})
            messages.append(
                {"role": "user", "content": f"Invalid format: {e}. Try again."})
            steps_taken += 1
            continue

        messages.append({"role": "assistant", "content": raw})

        if step.action == "final_answer":
            return {"decision": step.final_decision, "steps_taken": steps_taken + 1}

        if step.action == "escalate":
            return {"decision": step.final_decision or "Escalate for Senior Review",
                    "steps_taken": steps_taken + 1}

        if step.action in ALLOWED_TOOLS:
            tool_fn = ALLOWED_TOOLS[step.action]
            result = tool_fn(case)
            messages.append({
                "role": "user",
                "content": f"Tool result: {json.dumps(result)}"
            })
        else:
            messages.append({
                "role": "user",
                "content": "That action is not in the allow-list. Choose a valid one."
            })

        steps_taken += 1

    return {"decision": "Escalate for Senior Review", "reason": "MAX_STEPS exceeded"}
