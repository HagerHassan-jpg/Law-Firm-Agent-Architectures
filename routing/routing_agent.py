import os
from dotenv import load_dotenv
from google import genai
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.tools import (
    load_case
)


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

#Promet for Gemini
SYSTEM_PROMPT = """
You are a legal case analyzer.

Analyze the case according to the business rules.

DO NOT make the final decision.

Evaluate ONLY these four categories:

1. Documents
2. Conflict
3. Specialist
4. Client History

Return ONLY valid JSON.

Possible values:

documents:
- complete
- missing_secondary_urgent
- missing_secondary_not_urgent
- missing_critical

conflict:
- none
- confirmed
- suspected_strong
- suspected_weak

specialist:
- exact_available
- assign_related
- escalate

client_history:
- reuse_document
- request_document

Return this exact format:

{
  "documents": "",
  "conflict": "",
  "specialist": "",
  "client_history": ""
}
"""

# use Gemini
def analyze_case(case):

    prompt = f"""
{SYSTEM_PROMPT}

Case:

{json.dumps(case, indent=2)}
"""
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    return json.loads(response.text)


# Decision
def final_decision(result):

    if result["conflict"] == "confirmed":
        return "Reject Due to Conflict of Interest"

    if result["conflict"] == "suspected_weak":
        return "Escalate for Senior Review"

    if result["documents"] == "missing_critical":
        return "Request More Information"

    if result["documents"] == "missing_secondary_urgent":
        return "Provisionally Accept and Request Missing Documents"

    if result["specialist"] == "assign_related":
        return "Assign to Related Specialist"

    if result["specialist"] == "escalate":
        return "Escalate Due to No Available Specialist"

    return "Accept Case"



# Test the Agent 
if __name__ == "__main__":
    
    test_ids = ["CASE-001", "CASE-002", "CASE-003", "CASE-004"]

    for case_id in test_ids:
        case = load_case(case_id)

        print(f"\n--- {case_id} ---")

        analysis = analyze_case(case)

        print("Gemini Analysis:")
        print(json.dumps(analysis, indent=4))

        decision = final_decision(analysis)

        print("\nFinal Decision:")
        print(decision)