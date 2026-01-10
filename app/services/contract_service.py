import os
import shutil
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from app.models.contract import Contract, ContractStatus
from app.models.user import User
from app.utils.helpers import extract_text_from_file
from app.config import settings
from typing import List

class ContractService:
    @staticmethod
    async def upload_contract(
        db: Session,
        user: User,
        file: UploadFile,
        title: str
    ) -> Contract:
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{user.id}_{int(datetime.utcnow().timestamp())}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving file: {str(e)}"
            )
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Extract text
        try:
            content = extract_text_from_file(file_path, file.content_type)
        except Exception as e:
            content = None
        
        # Create contract record
        contract = Contract(
            user_id=user.id,
            title=title,
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file.content_type,
            content=content,
            status=ContractStatus.UPLOADED
        )
        
        db.add(contract)
        db.commit()
        db.refresh(contract)
        return contract
    
    @staticmethod
    def get_user_contracts(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Contract]:
        return db.query(Contract).filter(Contract.user_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_contract(db: Session, contract_id: int, user_id: int) -> Contract:
        contract = db.query(Contract).filter(
            Contract.id == contract_id,
            Contract.user_id == user_id
        ).first()
        
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )
        
        return contract
    
    @staticmethod
    def delete_contract(db: Session, contract_id: int, user_id: int) -> bool:
        contract = ContractService.get_contract(db, contract_id, user_id)
        
        # Delete file
        if os.path.exists(contract.file_path):
            os.remove(contract.file_path)
        
        # Delete from database
        db.delete(contract)
        db.commit()
        return True

from datetime import datetime
