from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from db import Base

class Priority(Enum):
    A = 1
    B = 2
    C = 3
    D = 4

class Category(Enum):
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'
    yearly = 'yearly'
    decade = 'decade'

class User(Base):
    __tablename__="users"

    id = Column('id',Integer, primary_key=True, index=True)
    name = Column('name', String)
    email = Column('email', String, unique=True, index=True)
    password = Column('hashed_password', String)
    is_active = Column('is_active', Boolean, default=True)
    is_admin = Column('is_admin', Boolean, default=False)

    tasks = relationship("Task", back_populates="assigned_user")


class Task(Base):
    __tablename__ = "tasks"
    id = Column('id', Integer, primary_key=True, index=True)
    user_id = Column('user_id', Integer, ForeignKey("users.id"))
    priority = Column('priority', Priority)
    title = Column('title', String, index=True)
    assigned_user = relationship("User", back_populates="tasks")
    items = relationship("Item", back_populates="task_title")
    deadline = Column('deadline', datetime, default=None, nullable=False)
    date = Column('date', datetime, default=datetime.now(), nullable=False, server_default=datetime.current_timestamp())
    done = Column('done', Boolean, default=False, nullable=False)
 

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))

    task_title = relationship("Task", back_populates="tasks")

