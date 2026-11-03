from enum import Enum

from pydantic import BaseModel, Field


class Priority(str, Enum):
    haute = "haute"
    moyenne = "moyenne"
    basse = "basse"


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    priority: Priority = Priority.moyenne


class TaskUpdate(BaseModel):
    done: bool


class Task(BaseModel):
    id: int
    title: str
    priority: Priority
    done: bool