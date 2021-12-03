from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, time
from enum import Enum
from sql_app.models import Priority, Category

class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(BaseModel):
    id: int
    user_id: int
    task_id: int
class TaskBase(BaseModel):
    title: str
    priority: Enum
    category: Enum
    items: Optional[List[Item]] = []
    deadline: datetime
    created: datetime
    estimated_time: Optional[time] = None
    spent_time: Optional[time] = None
    class Config:
        orm_mode = True
class TaskCreate(TaskBase):
    pass
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
    tasks: List[Task] = []

    class Config:
        orm_mode = True

