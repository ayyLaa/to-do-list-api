from fastapi import APIRouter
from starlette.responses import JSONResponse

import storage

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

@router.get("/tasks")
async def tasks():
    return storage.get_all_items()

@router.get("/tasks/{id}")
async def task(id: int):
    task = storage.get_item(id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return task
