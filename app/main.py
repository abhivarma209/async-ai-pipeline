from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes.jobs import jobs_router
from app.routes.query import query_router

app = FastAPI(title="Async AI Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(query_router)
app.include_router(jobs_router)