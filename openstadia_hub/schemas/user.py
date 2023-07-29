from pydantic import BaseModel

from .server import Server


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    servers: list[Server] = []

    class Config:
        orm_mode = True
