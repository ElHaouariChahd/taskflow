from app.models import TaskCreate
from app.repository import TaskRepository


class TaskNotFound(Exception):
    pass


class TaskService:
    """Couche métier : applique les règles, sans connaître ni HTTP ni SQL."""

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def list_tasks(self, status: str = "all"):
        done = {"all": None, "active": False, "done": True}[status]
        return self.repo.list_tasks(done)

    def create_task(self, data: TaskCreate):
        title = data.title.strip()
        if not title:
            raise ValueError("Le titre ne peut pas être vide")
        return self.repo.create(title, data.priority.value)

    def set_done(self, task_id: int, done: bool):
        if self.repo.get(task_id) is None:
            raise TaskNotFound(task_id)
        return self.repo.update_done(task_id, done)

    def delete_task(self, task_id: int):
        if not self.repo.delete(task_id):
            raise TaskNotFound(task_id)