from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AgentActionStep(BaseModel):
    thought: str = Field(...)
    action: Optional[str] = Field(default=None)
    action_input: Optional[Dict[str, Any]] = Field(default_factory=dict)
    final_decision: Optional[str] = Field(default=None)
    flags: List[str] = Field(default_factory=list)
    reasoning: Optional[str] = Field(default=None)
    escalate: bool = Field(default=False)
