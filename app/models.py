from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, UUID, Text, String, DateTime
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    query        = Column(Text, nullable=False)
    state        = Column(String, default="pending")
    result       = Column(Text, nullable=True)
    error        = Column(Text, nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
    started_at   = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)