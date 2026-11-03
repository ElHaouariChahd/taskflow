import pytest

from app.models import TaskCreate
from app.repository import TaskRepository
from app.service import TaskNotFound, TaskService


@pytest.fixture
def svc():
    return TaskService(TaskRepository(":memory:"))


def test_title_is_trimmed(svc):
    task = svc.create_task(TaskCreate(title="  Réviser Git  "))
    assert task["title"] == "Réviser Git"


def test_default_priority_is_moyenne(svc):
    assert svc.create_task(TaskCreate(title="A"))["priority"] == "moyenne"


def test_set_done_unknown_task_raises(svc):
    with pytest.raises(TaskNotFound):
        svc.set_done(999, True)