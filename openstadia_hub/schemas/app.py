from pydantic import BaseModel, ConfigDict


class App(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    command: str
    server_id: int
