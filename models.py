from datetime import datetime

from sqlalchemy.sql.sqltypes import Integer
 
from database import Base
 
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN
from enum import Enum
import hashlib
 
SQLITE3_NAME = "./db.sqlite3"
 
class Priority(int, Enum):
    a = 1
    b = 2
    c = 3
    d = 4

class Category(str, Enum):
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'
    yearly = 'yearly'
    decade = 'decade'

class User(Base):
    __tablename__ = 'user'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    username = Column('username', String(256))
    password = Column('password', String(256))
    mail = Column('mail', String(256))
 
    def __init__(self, username, password, mail):
        self.username = username
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.mail = mail
 
    def __str__(self):
        return str(self.id) + ':' + self.username
 
 
class Task(Base):
    __tablename__ = 'task'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
 
    user_id = Column('user_id', ForeignKey('user.id'))
    content = Column('content', String(256))
    deadline = Column(
        'deadline',
        DateTime,
        default=None,
        nullable=False,
    )
    created_at = Column(
        'created_at',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
    )
    priority = Column('priority', Integer, nullable=True)
    category = Column('category', String, nullable=True)
    done = Column('done', BOOLEAN, default=False, nullable=False)
 
    def __init__(self, user_id: int, content: str, deadline: datetime, priority: Priority, category: Category, created_at: datetime = datetime.now()):
        self.user_id = user_id
        self.content = content
        self.deadline = deadline
        self.created_at = created_at
        self.priority = priority
        self.category = category
        self.done = False
 
    def __str__(self):
        return str(self.id) + \
            ': user_id -> ' + str(self.user_id) + \
            ', content -> ' + self.content + \
            ', deadline -> ' + self.deadline.strftime('%Y/%m/%d - %H:%M:%S') + \
            ', priority -> ' + str(self.priority) + \
            ', category -> ' + str(self.category) + \
            ', created_at -> ' + self.created_at.strftime('%Y/%m/%d - %H:%M:%S') + \
            ', done -> ' + str(self.done)