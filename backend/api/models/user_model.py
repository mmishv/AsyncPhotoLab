from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
