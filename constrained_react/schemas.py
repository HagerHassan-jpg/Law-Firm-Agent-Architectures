from pydantic import BaseModel
from typing import Literal, Optional


class AgentStep(BaseModel):
    thought: str
    action: Literal[
        "evaluate_documents",
        "evaluate_conflict",
        "evaluate_specialist",
        "evaluate_client_history",
        "final_answer",
        "escalate",
    ]
    action_input: Optional[dict] = None
    final_decision: Optional[str] = None
