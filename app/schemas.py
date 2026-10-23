from enum import Enum
from pydantic import BaseModel, Field

class Urgency(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Intent(str, Enum):
    refund = "refund"
    order_status = "order_status"
    complaint = "complaint"
    technical_issue = "technical_issue"
    other = "other"

class SupportAnalysis(BaseModel):
    issue_summary: str = Field(description="One-sentence summary of the problem")
    intent: Intent
    urgency: Urgency
    suggested_reply: str = Field(description="Professional, empathetic reply to the customer")
    needs_human: bool = Field(description="True if a human agent should take over")