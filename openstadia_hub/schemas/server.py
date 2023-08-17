from pydantic import BaseModel, ConfigDict


class ServerBase(BaseModel):
    name: str


class ServerCreate(ServerBase):
    pass


class Server(ServerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    token: str
    owner_id: int
