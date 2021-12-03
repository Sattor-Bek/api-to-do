from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from datetime import datetime, time
from .database import Base
from enum import Enum
class Priority(Enum):
    a = 1
    b = 2
    c = 3
    d = 4

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
    priority = Column('priority', Integer)
    category = Column('category', String)
    title = Column('title', String)
    assigned_user = relationship("User", back_populates="tasks")
    items = relationship("Item", back_populates="task_title")
    deadline = Column('deadline', DateTime, default=None, nullable=False)
    created = Column('created', DateTime, default=datetime.now(), nullable=False, server_default=current_timestamp())
    estimated_time = Column('estimated_time', Integer, default=0, nullable=True)
    spent_time = Column('spent_time', Integer, default=0, nullable=True)

    done = Column('done', Boolean, default=False, nullable=False)
 

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))

    task_title = relationship("Task", back_populates="tasks")

