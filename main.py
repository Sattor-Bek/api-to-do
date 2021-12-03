from fastapi import Depends, FastAPI, HTTPException, security, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from typing import Optional
from database import Task, User, engine
from passlib.context import CryptContext
from jose import JWTError, jwt

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")
form = security.OAuth2PasswordRequestForm
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
class UserIn(BaseModel):
    name: str
    email: str
    password: str
class TaskIn(BaseModel):
    title: str
    done: bool

class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: Optional[str] = None

def get_task(db_session: Session, task_id: int):
    return db_session.query(Task).filter(Task.id == task_id).first()
def get_task_by_user(db_session: Session, user_id: int):
    return db_session.query(Task).filter(Task.user_id == user_id).all()
def get_user(db_session: Session, user_id: int):
    return db_session.query(User).filter(User.id == user_id).first()
def get_db(request: Request):
    return request.state.db


app = FastAPI()

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)

def get_user_by_username(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserIn(**user_dict)

# def authenticate_user(db, username: str, password: str):
#     user = get_user_by_username(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.password):
#         return False
#     return user

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: form = Depends()):
#     user = authenticate_user(get_db(), form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires # The JWT specification says that there's a key sub, with the subject of the token.
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/{user_id}/tasks/")
async def read_user_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = get_task_by_user(db, user_id)
    return tasks

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    return user

@app.post("/users/")
async def create_user(user_in: UserIn,  db: Session = Depends(get_db)):
    user = User(
        name=user_in.name, 
        email=user_in.email, 
        password=user_in.password,
        )
    db.add(user)
    db.commit()
    user = get_user(db, user.id)
    return user

# @app.post("/tasks/")
# async def create_task(task_in: TaskIn,  db: Session = Depends(get_db)):
#     task = Task(title=task_in.title, done=False)
#     db.add(task)
#     db.commit()
#     task = get_task(db, task.id)
#     return task

@app.put("/users/{user_id}")
async def update_user(user_id: int, User_in: UserIn, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    user.title = User_in.title
    db.commit()
    user = get_user(db, user_id)
    return user

# @app.delete("/users/{user_id}")
# async def delete_user(task_id: int, db: Session = Depends(get_db)):
#     task = get_task(db, task_id)
#     db.delete(task)
#     db.commit()

@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

@app.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    return task

@app.post("/tasks/")
async def create_task(task_in: TaskIn,  db: Session = Depends(get_db)):
    task = Task(title=task_in.title, done=False)
    db.add(task)
    db.commit()
    task = get_task(db, task.id)
    return task

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_in: TaskIn, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    task.title = task_in.title
    task.done = task_in.done
    db.commit()
    task = get_task(db, task_id)
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    db.delete(task)
    db.commit()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response