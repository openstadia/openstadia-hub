from pydantic import BaseModel

ClientId = str


class Client(BaseModel):
    id: ClientId
    token: str
    title: str
