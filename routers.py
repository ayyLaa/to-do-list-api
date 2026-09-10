from os.path import exists

from fastapi import APIRouter
from rich import status
from starlette.responses import JSONResponse, Response

import storage
from schemas import TaskCreate, TaskUpdate
import services

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

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Task title cannot be empty"}
        )
    return services.create_new_task(task)

@router.put("/tasks/{id}")
async def update_task(id: int, task_update: TaskUpdate):
    task_updated = storage.get_item(id)

    if task_updated is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    if task_updated.title is None and task_updated.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Empty body not allowed"}
        )

    if task_updated.title is not None and not task_updated.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Task title cannot be empty"}
        )

    updated = services.update_task(id, task_update)
    return updated

@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    task_deleted = storage.get_item(id)
    if task_deleted is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    services.delete_task(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)