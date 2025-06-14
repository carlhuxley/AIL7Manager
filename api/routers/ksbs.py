
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from main import get_db
from database.models.postgres_models import KSB
from api.schemas.ksb_schemas import KSBCreate, KSBResponse

router = APIRouter(prefix="/ksbs", tags=["KSBs"])

@router.get("/", response_model=List[KSBResponse])
def get_all_ksbs(db: Session = Depends(get_db)):
    """Get all KSBs with evidence count"""
    ksbs = db.query(KSB).all()
    ksb_responses = []
    
    for ksb in ksbs:
        evidence_count = len(ksb.evidence_links)
        ksb_responses.append(KSBResponse(
            id=ksb.id,
            code=ksb.code,
            description=ksb.description,
            evidence_count=evidence_count
        ))
    
    return ksb_responses

@router.post("/", response_model=KSBResponse)
def create_ksb(ksb: KSBCreate, db: Session = Depends(get_db)):
    """Create a new KSB"""
    # Check if KSB code already exists
    existing_ksb = db.query(KSB).filter(KSB.code == ksb.code).first()
    if existing_ksb:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"KSB with code {ksb.code} already exists"
        )
    
    db_ksb = KSB(code=ksb.code, description=ksb.description)
    db.add(db_ksb)
    db.commit()
    db.refresh(db_ksb)
    
    return KSBResponse(
        id=db_ksb.id,
        code=db_ksb.code,
        description=db_ksb.description,
        evidence_count=0
    )

@router.get("/{ksb_id}", response_model=KSBResponse)
def get_ksb(ksb_id: int, db: Session = Depends(get_db)):
    """Get a specific KSB by ID"""
    ksb = db.query(KSB).filter(KSB.id == ksb_id).first()
    if not ksb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KSB not found"
        )
    
    evidence_count = len(ksb.evidence_links)
    return KSBResponse(
        id=ksb.id,
        code=ksb.code,
        description=ksb.description,
        evidence_count=evidence_count
    )
