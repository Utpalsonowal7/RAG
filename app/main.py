from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.routes.doc import router as upload_docs
from app.routes.exam import router as exam_router
from app.routes.doc_db import router as db_docs
from contextlib import asynccontextmanager
from app.db.db import engine,Base
from app.db.models import Document,DocumentChunk

@asynccontextmanager
async def lifespan(app:FastAPI):
     async with engine.begin() as conn:
          await conn.run_sync(Base.metadata.create_all)

     yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_router = APIRouter(prefix="/api")

api_router.include_router(upload_docs)
api_router.include_router(exam_router)
api_router.include_router(db_docs)

app.include_router(api_router)


@app.get("/")
def root():
    return {"status : ok"}
