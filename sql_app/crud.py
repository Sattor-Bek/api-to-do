from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tasks(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int, items: Optional[List[models.Item]]):
    if items:
        db_task = models.Task(**task.dict(), user_id=user_id, items=items)
    else:
        db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_items(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_task_item(db: Session, task_id: int, user_id: int, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict(), task_id=task_id, user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

