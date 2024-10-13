from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    logging_level: str
    celery_broker: str = 'pyamqp://guest:guest@localhost:5672'
    celery_backend: str = 'db+postgresql://postgres:password@localhost:5432/celery_logs?sslmode=disable'

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()