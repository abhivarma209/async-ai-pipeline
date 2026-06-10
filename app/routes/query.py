import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job
from app.schemas import JobCreate, JobStatusResponse
from app.worker.tasks import process_job

query_router = APIRouter()


@query_router.post("/query", response_model=JobStatusResponse)
def run_query(payload: JobCreate, db: Session = Depends(get_db)):
    try:
        job_id = uuid.uuid4()
        job_obj = Job(
            id=job_id,
            query=payload.query,
        )
        db.add(job_obj)
        db.commit()

        process_job.delay(str(job_id))

        return JobStatusResponse(id=job_obj.id, state=job_obj.state)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))