from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class AnalysisResponse(BaseModel):
    id: int
    contract_id: int
    analysis_type: str
    summary: Optional[str]
    key_terms: Optional[List[Dict[str, Any]]]
    risk_score: Optional[float]
    risks: Optional[List[Dict[str, Any]]]
    recommendations: Optional[List[str]]
    clauses: Optional[List[Dict[str, Any]]]
    parties_involved: Optional[List[str]]
    obligations: Optional[List[Dict[str, Any]]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatMessageCreate(BaseModel):
    contract_id: int
    message: str

class ChatMessageResponse(BaseModel):
    id: int
    contract_id: int
    user_id: int
    message: str
    response: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
