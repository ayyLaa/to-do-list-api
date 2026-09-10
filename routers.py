from fastapi import APIRouter
from pygments.lexer import default

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/")
async def root():
    return{
        "name": "Task API",
        "version": "1.0",
        "endpoinnts" : ["/tasks"]
    }

@router.get("/health")
async def health():
    return {"status": "ok"}