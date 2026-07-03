from celery import Celery
from sqlalchemy.orm import Session
from openai import OpenAI
from datetime import datetime

from app.database import SessionLocal
from app.models import Job
from config import settings

# Celery app instance
celery_app = Celery(
    "pipeline",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)


@celery_app.task(bind=True, max_retries=3)
def process_job(self, job_id: str):
    db: Session = SessionLocal()

    try:
        # 1. fetch job
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return

        # 2. mark running
        job.state = "running"
        job.started_at = datetime.utcnow()
        db.commit()

        # 3. call OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Summarize the following text concisely."
                },
                {
                    "role": "user",
                    "content": job.query
                }
            ]
        )

        summary = response.choices[0].message.content

        # 4. store result
        job.state = "success"
        job.result = summary
        job.completed_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        # 5. handle failure
        if job:
            job.state = "failed"
            job.error = str(e)
            job.completed_at = datetime.utcnow()
            db.commit()

        # retry with exponential backoff: 1s, 2s, 4s
        raise self.retry(exc=e, countdown=2 ** self.request.retries)

    finally:
        db.close()