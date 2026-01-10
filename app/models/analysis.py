from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    analysis_type = Column(String)  # 'full', 'risk', 'summary'
    summary = Column(Text)
    key_terms = Column(JSON)
    risk_score = Column(Float)
    risks = Column(JSON)
    recommendations = Column(JSON)
    clauses = Column(JSON)
    parties_involved = Column(JSON)
    obligations = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    contract = relationship("Contract", back_populates="analyses")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    contract = relationship("Contract", back_populates="chat_messages")
    user = relationship("User")
