import pytest
from fastapi.testclient import TestClient

from app.main import app, get_service
from app.repository import TaskRepository
from app.service import TaskService


@pytest.fixture
def client():
    test_service = TaskService(TaskRepository(":memory:"))
    app.dependency_overrides[get_service] = lambda: test_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_task(client):
    r = client.post("/api/tasks", json={"title": "Réviser Git", "priority": "haute"})
    assert r.status_code == 201
    assert r.json()["done"] is False


def test_empty_title_rejected(client):
    assert client.post("/api/tasks", json={"title": "   "}).status_code == 422


def test_list_and_filter(client):
    a = client.post("/api/tasks", json={"title": "A"}).json()
    client.post("/api/tasks", json={"title": "B"})
    client.patch(f"/api/tasks/{a['id']}", json={"done": True})
    assert len(client.get("/api/tasks").json()) == 2
    assert len(client.get("/api/tasks?status=done").json()) == 1
    assert len(client.get("/api/tasks?status=active").json()) == 1


def test_delete_task(client):
    t = client.post("/api/tasks", json={"title": "A supprimer"}).json()
    assert client.delete(f"/api/tasks/{t['id']}").status_code == 204
    assert client.delete(f"/api/tasks/{t['id']}").status_code == 404