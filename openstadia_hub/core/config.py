from pydantic import BaseSettings


class Settings(BaseSettings):
    auth0_domain: str
    auth0_audience: str

    class Config:
        env_file = ".env"


settings = Settings()
