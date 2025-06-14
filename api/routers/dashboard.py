
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pymongo.database import Database
from typing import List, Dict, Any
from main import get_db, get_mongo_db
from database.models.postgres_models import KSB, EvidenceKSBLink
from api.schemas.ksb_schemas import KSBResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/overview")
def get_dashboard_overview(
    user_id: int,
    db: Session = Depends(get_db),
    mongo_db: Database = Depends(get_mongo_db)
) -> Dict[str, Any]:
    """Get dashboard overview with KSB progress and stats"""
    
    # Get all KSBs with evidence counts
    ksbs = db.query(KSB).all()
    ksb_progress = []
    
    total_evidence_count = 0
    covered_ksbs = 0
    
    for ksb in ksbs:
        evidence_count = len(ksb.evidence_links)
        total_evidence_count += evidence_count
        
        if evidence_count > 0:
            covered_ksbs += 1
            
        ksb_progress.append({
            "id": ksb.id,
            "code": ksb.code,
            "description": ksb.description,
            "evidence_count": evidence_count,
            "status": "covered" if evidence_count > 0 else "not_covered"
        })
    
    # Get total evidence for user
    user_evidence_count = mongo_db.evidence.count_documents({"user_id": user_id})
    
    # Calculate coverage percentage
    total_ksbs = len(ksbs)
    coverage_percentage = (covered_ksbs / total_ksbs * 100) if total_ksbs > 0 else 0
    
    return {
        "user_id": user_id,
        "stats": {
            "total_ksbs": total_ksbs,
            "covered_ksbs": covered_ksbs,
            "coverage_percentage": round(coverage_percentage, 1),
            "total_evidence": user_evidence_count,
            "total_evidence_links": total_evidence_count
        },
        "ksb_progress": ksb_progress
    }
