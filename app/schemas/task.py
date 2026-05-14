from pydantic import BaseModel


class TaskModel(BaseModel):
    title: str
    notes: str
    deadline: str | None = None  # RFC 3339
