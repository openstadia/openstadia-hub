from pydantic import BaseModel, ConfigDict

from .server import Server


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    servers: list[Server] = []
