import json

import bcrypt
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from ...api.models.user_model import User, UserCreate
from ...api.utils.user import get_current_user, authenticate_user, get_user_by_email, UserAlreadyExistsException, \
    InvalidCredentialsException, create_tokens_for_user
from ..config.redis_config import redis_client

router = APIRouter()

security = HTTPBasic()


@router.post("/register/")
async def register_user(user: UserCreate):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise UserAlreadyExistsException(user.email)

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
    password_hash = hashed_password.decode("utf-8")

    user_data = {"id": redis_client.incr("user_id"), "email": user.email, "hashed_password": password_hash,
                 "first_name": user.first_name, "last_name": user.last_name, "is_active": True, "is_superuser": False, }
    redis_client.set(user.email, json.dumps(user_data))

    access_token, refresh_token = create_tokens_for_user(User(**user_data))
    user = User(**user_data)
    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}


@router.post("/login/")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_by_email(credentials.username)
    if user is None or not bcrypt.checkpw(credentials.password.encode("utf-8"), user.hashed_password.encode("utf-8")):
        raise InvalidCredentialsException()

    access_token, refresh_token = create_tokens_for_user(user)
    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}


@router.post("/token/")
async def login_for_access_token(credentials: HTTPBasicCredentials = Depends(security)):
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise InvalidCredentialsException()

    access_token, refresh_token = create_tokens_for_user(user)
    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}


@router.get("/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout/")
async def logout(email: str):
    redis_client.delete(email + "_refresh_token")
    return {"message": "Successfully logged out"}
