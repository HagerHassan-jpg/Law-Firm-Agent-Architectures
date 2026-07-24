#load
import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent  / "test_cases.json"


def load_case(case_id):

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        cases = json.load(file)

    for case in cases:
        if case["case_id"] == case_id:
            return case

    return None



#1
def evaluate_documents(case):

    if case is None:
        return {"error": "Case not found"}

    return {
        "document_status": case["document_status"],
        "days_until_deadline": case["days_until_deadline"],
        "is_urgent": case["days_until_deadline"] <= 7
    } 


#2
def evaluate_conflict(case):

    if case is None:
        return {"error": "Case not found"}

    return {
        "conflict_status": case["conflict_status"],
        "evidence_strength": case["evidence_strength"]
    }


#3
def evaluate_specialist(case):

    if case is None:
        return {"error": "Case not found"}

    return {
        "exact_specialist_available": case["exact_specialist_available"],
        "related_specialist_available": case["related_specialist_available"],
        "is_high_priority": case["days_until_deadline"] <= 3
    }

#4
def evaluate_client_history(case):

    if case is None:
        return {"error": "Case not found"}

    return {
        "returning_client": case["returning_client"],
        "document_available_in_archive": case["document_available_in_archive"]
    }