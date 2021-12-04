import hashlib
import database

from models import User
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException

def auth(credential):
    username = credential.username
    password = hashlib.md5(credential.password.encode()).hexdigest()

    user = database.session.query(User).filter(User.username == username).first()
    database.session.close()

    if user is None or user.password != password:
        error = "Wrong password or user name"
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={'WWW-Authenticate': "Basic"}
        )
    return username
