from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.services.auth import get_current_user
from app.models.todo import ToDo
from app.models.user import User
from app.schemas.todo import ToDoCreate, ToDoUpdate, ToDoOut

router = APIRouter(prefix="/todos", tags=["todos"])

router.get("/", response_model=List[ToDoOut])
def list_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0,
    completed: bool | None = None,
    tag: str | None = None,
    q: str | None = None,
    due_before: datetime | None = None
):
    query = db.query(ToDo).filter(ToDo.owner_id == current_user.id)
    if completed is not None:
        query = query.filter(ToDo.completed == completed)
    if tag:
        query = query.filter(ToDo.tags.contains(tag))
    if q:
        query = query.filter(ToDo.title.contains(q))
    if due_before:
        query = query.filter(ToDo.due_date < due_before)

    return query.offset(offset).limit(limit).all()

@router.get("/{todo_id}", response_model=ToDoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(ToDo).filter(ToDo.id == todo_id, ToDo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.post("/", response_model=ToDoOut)
def create_todo(todo_data: ToDoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_todo = ToDo(**todo_data.dict(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.put("/{todo_id}", response_model=ToDoOut)
def update_todo(todo_id: int, update_data: ToDoUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(ToDo).filter(ToDo.id == todo_id, ToDo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(ToDo).filter(ToDo.id == todo_id, ToDo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return
