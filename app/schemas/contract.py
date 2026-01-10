from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ContractBase(BaseModel):
    title: str

class ContractCreate(ContractBase):
    pass

class ContractResponse(ContractBase):
    id: int
    user_id: int
    filename: str
    file_size: Optional[int]
    file_type: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ContractList(BaseModel):
    contracts: list[ContractResponse]
    total: int
