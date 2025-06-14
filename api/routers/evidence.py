
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database
from sqlalchemy.orm import Session
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from main import get_db, get_mongo_db
from database.models.postgres_models import EvidenceKSBLink, KSB
from api.schemas.evidence_schemas import EvidenceCreate, EvidenceResponse, EvidenceUpdate

router = APIRouter(prefix="/evidence", tags=["Evidence"])

@router.post("/", response_model=EvidenceResponse)
def create_evidence(
    evidence: EvidenceCreate,
    db: Session = Depends(get_db),
    mongo_db: Database = Depends(get_mongo_db)
):
    """Create new evidence entry"""
    
    # Create evidence document in MongoDB
    evidence_doc = {
        "user_id": evidence.user_id,
        "project_id": evidence.project_id,
        "title": evidence.title,
        "content_type": evidence.content_type,
        "content": evidence.content,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = mongo_db.evidence.insert_one(evidence_doc)
    evidence_id = str(result.inserted_id)
    
    # Create KSB links in PostgreSQL
    for ksb_id in evidence.ksb_ids:
        # Verify KSB exists
        ksb = db.query(KSB).filter(KSB.id == ksb_id).first()
        if not ksb:
            # Rollback MongoDB insert if KSB doesn't exist
            mongo_db.evidence.delete_one({"_id": result.inserted_id})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"KSB with id {ksb_id} not found"
            )
        
        link = EvidenceKSBLink(evidence_id=evidence_id, ksb_id=ksb_id)
        db.add(link)
    
    db.commit()
    
    # Get the created evidence
    created_evidence = mongo_db.evidence.find_one({"_id": result.inserted_id})
    
    return EvidenceResponse(
        id=evidence_id,
        user_id=created_evidence["user_id"],
        project_id=created_evidence.get("project_id"),
        title=created_evidence["title"],
        content_type=created_evidence["content_type"],
        content=created_evidence["content"],
        ksb_ids=evidence.ksb_ids,
        created_at=created_evidence["created_at"],
        updated_at=created_evidence["updated_at"]
    )

@router.get("/", response_model=List[EvidenceResponse])
def get_evidence_list(
    user_id: Optional[int] = None,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db),
    mongo_db: Database = Depends(get_mongo_db)
):
    """Get list of evidence with optional filtering"""
    
    # Build MongoDB query
    query = {}
    if user_id:
        query["user_id"] = user_id
    if project_id:
        query["project_id"] = project_id
    
    evidence_docs = list(mongo_db.evidence.find(query))
    evidence_responses = []
    
    for doc in evidence_docs:
        evidence_id = str(doc["_id"])
        
        # Get KSB links from PostgreSQL
        ksb_links = db.query(EvidenceKSBLink).filter(
            EvidenceKSBLink.evidence_id == evidence_id
        ).all()
        ksb_ids = [link.ksb_id for link in ksb_links]
        
        evidence_responses.append(EvidenceResponse(
            id=evidence_id,
            user_id=doc["user_id"],
            project_id=doc.get("project_id"),
            title=doc["title"],
            content_type=doc["content_type"],
            content=doc["content"],
            ksb_ids=ksb_ids,
            created_at=doc["created_at"],
            updated_at=doc["updated_at"]
        ))
    
    return evidence_responses

@router.get("/{evidence_id}", response_model=EvidenceResponse)
def get_evidence(
    evidence_id: str,
    db: Session = Depends(get_db),
    mongo_db: Database = Depends(get_mongo_db)
):
    """Get specific evidence by ID"""
    
    try:
        doc = mongo_db.evidence.find_one({"_id": ObjectId(evidence_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid evidence ID format"
        )
    
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found"
        )
    
    # Get KSB links
    ksb_links = db.query(EvidenceKSBLink).filter(
        EvidenceKSBLink.evidence_id == evidence_id
    ).all()
    ksb_ids = [link.ksb_id for link in ksb_links]
    
    return EvidenceResponse(
        id=evidence_id,
        user_id=doc["user_id"],
        project_id=doc.get("project_id"),
        title=doc["title"],
        content_type=doc["content_type"],
        content=doc["content"],
        ksb_ids=ksb_ids,
        created_at=doc["created_at"],
        updated_at=doc["updated_at"]
    )
