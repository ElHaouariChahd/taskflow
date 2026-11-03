import os
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from app.models import Task, TaskCreate, TaskUpdate
from app.repository import TaskRepository
from app.service import TaskNotFound, TaskService

app = FastAPI(title="TaskFlow API", version="1.0.0")
service = TaskService(TaskRepository(os.getenv("DB_PATH", "taskflow.db")))


def get_service() -> TaskService:
    """Injection de dépendances : les tests remplacent ce service."""
    return service


@app.get("/api/tasks", response_model=list[Task])
def list_tasks(status: Literal["all", "active", "done"] = "all",
               svc: TaskService = Depends(get_service)):
    return svc.list_tasks(status)


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate, svc: TaskService = Depends(get_service)):
    try:
        return svc.create_task(data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.patch("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate, svc: TaskService = Depends(get_service)):
    try:
        return svc.set_done(task_id, data.done)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Tâche introuvable")


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, svc: TaskService = Depends(get_service)):
    try:
        svc.delete_task(task_id)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Tâche introuvable")


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")