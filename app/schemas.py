from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class JobCreate(BaseModel):
    query: str


class JobResponse(BaseModel):
    id: UUID
    query: str
    state: str
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobStatusResponse(BaseModel):
    id: UUID
    state: str