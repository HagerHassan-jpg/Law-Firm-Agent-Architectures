from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Case:
    case_id: str
    case_type: str
    days_until_deadline: int
    document_status: str
    evidence_strength: str
    conflict_status: str
    exact_specialist_available: bool
    related_specialist_available: bool
    returning_client: bool
    document_available_in_archive: bool

# Allowed decisions
ACCEPT = "Accept Case"
PROVISIONAL_ACCEPT = "Provisionally Accept and Request Missing Documents"
REQUEST_INFO = "Request More Information"
REJECT_CONFLICT = "Reject Due to Conflict of Interest"
ESCALATE_SENIOR = "Escalate for Senior Review"
ESCALATE_SPECIALIST = "Escalate Due to No Available Specialist"    


def _result(case: Case, decision: str, flags: List[str], reason: str) -> Dict[str, Any]:
    return {
        "case_id": case.case_id,
        "decision": decision,
        "flags": flags,
        "reasoning": reason,
    }

#Thresholds
URGENT_DOCUMENT_THRESHOLD = 7
URGENT_SPECIALIST_THRESHOLD = 3


def evaluate_case(case: Case) -> Dict[str, Any]:
    
    flags: List[str] = []

    document_status = case.document_status

    if case.returning_client and case.document_available_in_archive:
        if document_status in ("missing_critical", "missing_secondary"):
            flags.append("archived_document_reused")
            document_status = "complete"

    # Priority 1: confirmed conflict of interest
    if case.conflict_status == "confirmed":
        return _result(
            case,
            REJECT_CONFLICT,
            flags,
            "Confirmed conflict of interest overrides every other factor."
        )

    
    if case.conflict_status == "suspected" and case.evidence_strength == "weak":
        return _result(
            case,
            ESCALATE_SENIOR,
            flags,
            "Suspected conflict combined with weak evidence requires senior review."
        )

    
    if case.conflict_status == "suspected":
        flags.append("conflict_suspicion_warning")

    
    # Priority 3: Missing Critical Documents
    if document_status == "missing_critical":
        return _result(
            case,
            REQUEST_INFO,
            flags,
            "Critical documents are missing; cannot proceed regardless of urgency."
        )

    
    # Priority 4: Missing Secondary Documents
    if document_status == "missing_secondary":

        if case.days_until_deadline <= URGENT_DOCUMENT_THRESHOLD:

            flags.append("missing_secondary_docs")

            return _result(
                case,
                PROVISIONAL_ACCEPT,
                flags,
                f"Secondary documents missing but deadline is <= {URGENT_DOCUMENT_THRESHOLD} days; provisionally accepted while documents are requested."
            )

        else:

            flags.append("missing_secondary_docs_not_urgent")

            return _result(
                case,
                REQUEST_INFO,
                flags,
                f"Secondary documents missing and deadline is not urgent (>{URGENT_DOCUMENT_THRESHOLD} days); documents are requested before proceeding."
            )

    # Priority 5 & 6: Specialist Availability
    if not case.exact_specialist_available:

        if (
            case.related_specialist_available
            and case.days_until_deadline <= URGENT_SPECIALIST_THRESHOLD
        ):

            flags.append("related_specialist_assigned")

        else:

            return _result(
                case,
                ESCALATE_SPECIALIST,
                flags,
                f"No exact specialist available and the conditions for assigning a related specialist (available + deadline <= {URGENT_SPECIALIST_THRESHOLD} days) are not met."
            )
        
    # Priority 7: Default Decision
    return _result(
        case,
        ACCEPT,
        flags,
        "All checks passed; case accepted."
    )

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.tools import load_case

if __name__ == "__main__":
    test_ids = ["CASE-001", "CASE-002", "CASE-003", "CASE-004"]

    for case_id in test_ids:
        case_data = load_case(case_id)

        sample = Case(
            case_id=case_data["case_id"],
            case_type=case_data["case_type"],
            days_until_deadline=case_data["days_until_deadline"],
            document_status=case_data["document_status"],
            evidence_strength=case_data["evidence_strength"],
            conflict_status=case_data["conflict_status"],
            exact_specialist_available=case_data["exact_specialist_available"],
            related_specialist_available=case_data["related_specialist_available"],
            returning_client=case_data["returning_client"],
            document_available_in_archive=case_data["document_available_in_archive"],
        )

        result = evaluate_case(sample)

        print("=" * 50)
        print("Case Evaluation Result")
        print("=" * 50)
        print(f"Case ID   : {result['case_id']}")
        print(f"Decision  : {result['decision']}")
        print(f"Flags     : {', '.join(result['flags']) if result['flags'] else 'None'}")
        print(f"Reasoning : {result['reasoning']}")
        print("=" * 50)