
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EvidenceBase(BaseModel):
    title: str
    content_type: str = "markdown"
    content: str

class EvidenceCreate(EvidenceBase):
    user_id: int
    project_id: Optional[int] = None
    ksb_ids: List[int] = []

class EvidenceUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    ksb_ids: Optional[List[int]] = None

class EvidenceResponse(EvidenceBase):
    id: str
    user_id: int
    project_id: Optional[int]
    ksb_ids: List[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
