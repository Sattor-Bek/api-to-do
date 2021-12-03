from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime, time
from enum import Enum
from database import Base

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
    created = Column('created', datetime, default=datetime.now(), nullable=False, server_default=datetime.current_timestamp())
    estimated_time = Column('estimated_time', time, default=time.now(), nullable=True)
    spent_time = Column('spent_time', time, default=time.now(), nullable=True)

    done = Column('done', Boolean, default=False, nullable=False)
 

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))

    task_title = relationship("Task", back_populates="tasks")

