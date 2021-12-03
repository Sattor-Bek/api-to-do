from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

SQLALCHEMY_DATABASE_URI = "sqlite:///./todo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, echo=True
)

Base = declarative_base()

class User(Base):
    __tablename__="users"

    id = Column('id',String, primary_key=True, index=True)
    name = Column('name', String)
    email = Column('email', String, unique=True, index=True)
    password = Column('password', String)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column('id', Integer, primary_key = True)
    title = Column('title', String(200))
    done = Column('done', Boolean, default=False)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))


Base.metadata.create_all(bind=engine)
