from pydantic import BaseModel, ConfigDict, computed_field

from openstadia_hub.services.connection import connection_manager
from .user_server_role import UserServerRole


class ServerBase(BaseModel):
    name: str


class ServerCreate(ServerBase):
    pass


class Server(ServerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int

    @computed_field
    @property
    def online(self) -> bool:
        return connection_manager.is_connected(self.id)


class ServerRole(Server):
    role: UserServerRole


class ServerSettings(Server):
    token: str


class ServerToken(BaseModel):
    token: str
