from calendar import calendar
from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
 
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse

import database
from models import User, Task
from auth import *

import re
pattern = re.compile(r'\w{2,100}') 
pattern_password = re.compile(r'\w{2,100}') 
pattern_mail = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$') 

from calendar_module import CalendarModule
from datetime import datetime, timedelta

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
    username = auth(credentials)
    user = database.session.query(User).filter(User.username == username).first()

    today = datetime.now()
    next_w = today + timedelta(days=7)

    database.session.close()
 
    tasks = database.session.query(Task).filter(Task.user_id == user.id).all()
    database.session.close()

    cal = CalendarModule(username, {task.deadline.strftime('%Y%m%d'): task.done for task in tasks})
    cal = cal.formatyear(today.year)

    links = [task.deadline.strftime('/todo/'+username+'/%Y/%m/%d') for task in tasks] 
    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'user': user,
                                       'tasks': tasks,
                                       'links': links,
                                       'calender': cal})

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

def detail(request: Request, username, year, month, day, credentials: RedirectResponse = Depends(security)):
    username_temp = auth(credentials)
    if username_temp != username:
        return RedirectResponse('/')

    if request.method == 'GET' or request.method == 'POST':
        user = database.session.query(User).filter(User.username == username).first()
        all_tasks = database.session.query(Task).filter(Task.user_id == user.id).all()
        tasks = list(filter(lambda task: todays_tasks, all_tasks))
        database.session.close()

        return templates.TemplateResponse('detail.html',
                                        {'request': request,
                                        'username': username,
                                        'year': year,
                                        'month': month,
                                        'day': day,
                                        'tasks': tasks})

def todays_tasks(tasks: Task):
    today = datetime.today().strftime('%Y%M%D')
    return tasks.deadline.strftime('%Y%M%D') == today

@app.post("/done/")
async def done(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    username = auth(credentials)
    id = request.query_params['id']
    if id:
        task = database.session.query(Task).filter(Task.id == id).first()
        if task.done:
            task.done = False
        else:
            task.done = True
        url = task.deadline.strftime('/todo/'+username+'/%Y/%m/%d')
        database.session.commit()
        database.session.close()
    return RedirectResponse(url=url)