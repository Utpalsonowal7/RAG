from fastapi import FastAPI,APIRouter

from app.routes.doc import router as upload_docs

app = FastAPI()

api_router=APIRouter(prefix="/api")

api_router.include_router(upload_docs)

app.include_router(api_router)

@app.get("/")
def root():
     return {"status : ok"}
