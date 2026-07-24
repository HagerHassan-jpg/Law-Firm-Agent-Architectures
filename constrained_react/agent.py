import os
import json
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_fixed

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.tools import (
    load_case,
    evaluate_documents,
    evaluate_conflict,
    evaluate_specialist,
    evaluate_client_history,
)
from schemas import AgentActionStep

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MAX_STEPS = 5

ALLOWED_TOOLS = {
    "evaluate_documents": evaluate_documents,
    "evaluate_conflict": evaluate_conflict,
    "evaluate_specialist": evaluate_specialist,
    "evaluate_client_history": evaluate_client_history,
}

SYSTEM_PROMPT = """
You are a Constrained ReAct Agent for legal case intake evaluation at Ashford & Kane LLP.

Your task is to evaluate cases step-by-step using ONLY the allowed tools:
- evaluate_documents
- evaluate_conflict
- evaluate_specialist
- evaluate_client_history

Allowed final decisions:
- Accept Case
- Provisionally Accept and Request Missing Documents
- Request More Information
- Reject Due to Conflict of Interest
- Escalate for Senior Review
- Escalate Due to No Available Specialist

In each step:
1. Provide your step reasoning in 'thought'.
2. Call ONE tool using 'action' from the allowed list, OR set 'final_decision' when ready.
3. If critical risk or conflict is confirmed, set 'escalate' to true.
"""

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def call_constrained_model(prompt_context: str) -> AgentActionStep:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_context,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=AgentActionStep,
            temperature=0.1,
        ),
    )
    return AgentActionStep.model_validate_json(response.text)


def run_constrained_agent(case_id: str):
    case_data = load_case(case_id)
    if not case_data:
        return {"error": f"Case {case_id} not found"}

    history = f"Evaluating Case:\n{json.dumps(case_data, indent=2)}\n"
    step_count = 0

    print(f"\n=== Running Constrained ReAct Agent for Case: {case_id} ===")

    while step_count < MAX_STEPS:
        step_count += 1
        print(f"\n--- Step {step_count} of {MAX_STEPS} ---")

        step_res: AgentActionStep = call_constrained_model(history)
        print(f"Thought: {step_res.thought}")

        if step_res.escalate:
            print("⚠️ Escalation Triggered.")
            return {
                "case_id": case_id,
                "status": "ESCALATED",
                "reasoning": step_res.reasoning or "High risk or unresolved ambiguity detected.",
                "flags": step_res.flags,
                "total_steps": step_count,
            }

        if step_res.final_decision:
            print(f"🎯 Final Decision: {step_res.final_decision}")
            return {
                "case_id": case_id,
                "status": "COMPLETED",
                "decision": step_res.final_decision,
                "flags": step_res.flags,
                "reasoning": step_res.reasoning,
                "total_steps": step_count,
            }

        action_name = step_res.action
        if action_name:
            if action_name not in ALLOWED_TOOLS:
                feedback = f"\nSystem Error: Tool '{action_name}' is not in the ALLOWED_TOOLS list."
                history += feedback
                continue

            tool_fn = ALLOWED_TOOLS[action_name]
            observation = tool_fn(case_data)

            print(f"Action: {action_name}")
            print(f"Observation: {observation}")

            history += f"\nThought: {step_res.thought}\nAction: {action_name}\nObservation: {json.dumps(observation)}\n"

    print(f"🚨 MAX_STEPS limit ({MAX_STEPS}) reached! Automated escalation fallback.")
    return {
        "case_id": case_id,
        "status": "ESCALATED",
        "reasoning": f"Agent reached max allowed reasoning steps ({MAX_STEPS}) without final decision.",
        "flags": ["MAX_STEPS_EXCEEDED"],
        "total_steps": step_count,
    }


if __name__ == "__main__":
    test_cases = ["CASE-001", "CASE-002", "CASE-003", "CASE-004"]
    for c_id in test_cases:
        res = run_constrained_agent(c_id)
        print(f"\nResult Summary:\n{json.dumps(res, indent=2)}\n" + "=" * 60)
