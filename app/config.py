from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    firebase_credentials: str
    frontend_url: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
