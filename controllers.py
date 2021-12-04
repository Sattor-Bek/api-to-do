from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
 
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED 
 
import database
from models import User, Task
 
import hashlib

import re
pattern = re.compile(r'\w{2,100}') 
pattern_password = re.compile(r'\w{2,100}') 
pattern_mail = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$') 


app = FastAPI(
    title='To Do App Using Fast API',
)

templates = Jinja2Templates(directory="templates")
jinja_env = templates.env   
security = HTTPBasic()

def index(request: Request):
    return templates.TemplateResponse(
        'index.html', {
        'request': request
        })

def admin(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = hashlib.md5(credentials.password.encode()).hexdigest()

    user = database.session.query(User).filter(User.username == username).first()
    task = database.session.query(Task).filter(Task.user_id == user.id).all() if user is not None else []
    database.session.close()

    if user is None or user.password != password:
        error = 'Wrong password or wrong user name'
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Basic"},
        )

    
    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'user': user,
                                       'task': task})

async def register(request: Request):
    if request.method == 'GET':
        return templates.TemplateResponse('register.html',
                                          {'request': request,
                                           'username': '',
                                           'error': []})
 
    if request.method == 'POST':
        data = await request.form()
        username = data.get('username')
        password = data.get('password')
        password_tmp = data.get('password_tmp')
        mail = data.get('mail')
        error = []
        tmp_user = database.session.query(User).filter(User.username == username).first()
 
        if tmp_user is not None:
            error.append('The same user name exsits')
        if password != password_tmp:
            error.append('The password doesn not match')
        if pattern.match(username) is None:
            error.append('a user name should be multiple latin alphabets or/and numbers up to 100 characters')
        if pattern_password.match(password) is None:
            error.append('a password should be from multiple latin alphabets or/and numbers up to 100 characters')
        if pattern_mail.match(mail) is None:
            error.append('please input email address')
        if error:
            return templates.TemplateResponse('register.html',
                                              {'request': request,
                                               'username': username,
                                               'error': error})

        user = User(username, password, mail)
        database.session.add(user)
        database.session.commit()
        database.session.close()
 
        return templates.TemplateResponse('complete.html',
                                          {'request': request,
                                           'username': username})