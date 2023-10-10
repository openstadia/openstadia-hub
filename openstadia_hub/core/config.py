from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    auth0_domain: str
    auth0_audience: str

    database_url: str


settings = Settings()
