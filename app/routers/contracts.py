from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.services.contract_service import ContractService
from app.schemas.contract import ContractResponse, ContractList
from typing import List

router = APIRouter(prefix="/api/contracts", tags=["Contracts"])

@router.post("/upload", response_model=ContractResponse)
async def upload_contract(
    file: UploadFile = File(...),
    title: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a new contract"""
    # Validate file type
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF, DOCX, and TXT files are allowed."
        )
    
    contract = await ContractService.upload_contract(db, current_user, file, title)
    return contract

@router.get("", response_model=ContractList)
async def get_contracts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all contracts for current user"""
    contracts = ContractService.get_user_contracts(db, current_user.id, skip, limit)
    total = len(contracts)
    
    return {"contracts": contracts, "total": total}

@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: int,
    current_user: User = Depends(get_current_
