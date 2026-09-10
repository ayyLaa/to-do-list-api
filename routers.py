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
    """
        Returns API metadata including the name, version, and available endpoints.
    """
    return{
        "name": "Task API",
        "version": "1.0",
        "endpoinnts" : ["/tasks"]
    }

@router.get("/health")
async def health():
    """
        Checks the health status of the API to ensure the server is running successfully.
    """
    return {"status": "ok"}

@router.get("/tasks")
async def tasks():
    """
        Retrieves a list of all existing tasks from the database.
    """
    return storage.get_all_items()

@router.get("/tasks/{id}")
async def task(id: int):
    """
        Retrieves a specific task by its unique ID. Returns a 404 error if not found.
    """
    task = storage.get_item(id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return task

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """
        Creates a new task. The task title is required, and the 'done' status is set to false by default.
    """
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Task title cannot be empty"}
        )
    return services.create_new_task(task)

@router.put("/tasks/{id}")
async def update_task(id: int, task_update: TaskUpdate):
    """
        Updates an existing task. You can update the title, the 'done' status, or both.
    """
    task_updated = storage.get_item(id)

    if task_updated is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    if task_update.title is None and task_update.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Empty body not allowed"}
        )

    if task_update.title is not None and not task_update.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Task title cannot be empty"}
        )

    updated = services.update_task(id, task_update)
    return updated

@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    """
        Permanently deletes a task by its ID. Returns a 204 No Content status on success.
    """
    task_deleted = storage.get_item(id)
    if task_deleted is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    services.delete_task(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)