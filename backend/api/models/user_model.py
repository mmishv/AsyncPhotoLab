from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    is_active: bool
    is_superuser: bool
