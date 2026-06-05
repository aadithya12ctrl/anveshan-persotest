from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: Environment = Environment.DEVELOPMENT
    secret_key: str = "change-me-in-production"
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/agentic_layer"
    redis_url: str = "redis://localhost:6379/0"

    @property
    def is_development(self) -> bool:
        return self.app_env == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        return self.app_env == Environment.PRODUCTION

    @property
    def debug(self) -> bool:
        return not self.is_production


settings = Settings()