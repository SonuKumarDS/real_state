from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Real Estate AI Platform"
    secret_key: str = "change-this-in-production"
    database_url: str = "sqlite:///./realestate.db"
    cors_origins: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
