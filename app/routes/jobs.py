from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job
from app.schemas import JobResponse

jobs_router = APIRouter(prefix="/jobs")


@jobs_router.get("/{id}", response_model=JobResponse)
def get_job_by_id(id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@jobs_router.get("", response_model=list[JobResponse])
def get_jobs(state: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Job)
    if state:
        query = query.filter(Job.state == state)
    return query.all()