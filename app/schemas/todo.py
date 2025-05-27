from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ToDoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    due_date: Optional[datetime] = None
    tags: Optional[str] = None

class ToDoCreate(ToDoBase):
    pass

class ToDoUpdate(ToDoBase):
    title: Optional[str]
    description: Optional[str]
    completed: Optional[bool]
    due_date: Optional[datetime] = None
    tags: Optional[str] = None

class ToDoOut(ToDoBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True
