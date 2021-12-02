from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, time
from sql_app.models import Priority


class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Item(BaseModel):
    id: int
    user_id: int
    task_id: int
class TaskBase(BaseModel):
    title: str
    priority: Priority
    items: Optional[List[Item]] = None
    deadline: datetime
    created: datetime
    estimated_time: Optional[time]
    spent_time: Optional[time]
    class Config:
        orm_mode = True
class Task(TaskBase):
    id: int
    user_id: int

class UserBase(BaseModel):
    name: str
class UserBase(BaseModel):
    email: str
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: List[Task] = []

    class Config:
        orm_mode = True