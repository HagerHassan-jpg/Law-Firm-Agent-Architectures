from dataclasses import dataclass

@dataclass
class case:
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
