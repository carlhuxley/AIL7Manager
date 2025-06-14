
from pydantic import BaseModel
from typing import Optional

class KSBBase(BaseModel):
    code: str
    description: str

class KSBCreate(KSBBase):
    pass

class KSBResponse(KSBBase):
    id: int
    evidence_count: int
    
    class Config:
        from_attributes = True
