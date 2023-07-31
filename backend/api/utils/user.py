import json
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from starlette import status

from api.models.user_model import User
from api.routers.auth import security
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, redis_client, REFRESH_TOKEN_EXPIRE_DAYS


class UserAlreadyExistsException(HTTPException):
    def __init__(self, email):
        detail = f"Пользователь с email '{email}' уже зарегистрирован."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        detail = "Неверные учетные данные"
        headers = {"WWW-Authenticate": "Basic"}
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)


def get_user_by_email(email: str) -> Optional[User]:
    user_data = redis_client.get(email)

    if user_data:
        user = User(**json.loads(user_data))
        return user
    else:
        return None


def authenticate_user(email: str, password: str) -> Optional[User]:
    user = get_user_by_email(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        return user
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> Optional[User]:
    user = authenticate_user(credentials.username, credentials.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_expiration = redis_client.ttl(user.id)
    if token_expiration < 0:
        raise HTTPException(status_code=401, detail="Token has expired")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> Optional[User]:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
