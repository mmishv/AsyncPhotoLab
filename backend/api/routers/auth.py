import json
import uuid
from datetime import timedelta, datetime

import bcrypt
import jwt
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from api.models.user_model import User
from config.settings import (redis_client, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, )
from api.utils.user import get_current_user, authenticate_user, get_user_by_email, create_access_token, \
    create_refresh_token, UserAlreadyExistsException, InvalidCredentialsException

router = APIRouter()

security = HTTPBasic()


@router.post("/register/", response_model=User)
async def register_user(user: User):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise UserAlreadyExistsException(user.email)

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
    user.password_hash = hashed_password.decode("utf-8")

    user.id = str(uuid.uuid4())

    user_data = json.dumps(user.model_dump())
    redis_client.set(user.email, user_data)
    return user


@router.post("/login/")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_by_email(credentials.username)
    if user is None or not bcrypt.checkpw(credentials.password.encode("utf-8"), user.password_hash.encode("utf-8")):
        raise InvalidCredentialsException()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {"sub": user.email, "exp": datetime.utcnow() + access_token_expires, }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token/")
async def login_for_access_token(credentials: HTTPBasicCredentials = Depends(security)):
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise InvalidCredentialsException()

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout/")
async def logout(current_user: User = Depends(get_current_user)):
    redis_client.set(current_user.email, "", ex=0)
    return {"message": "Logged out successfully"}
