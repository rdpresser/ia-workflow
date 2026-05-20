from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Shared config: all settings classes read from the same .env file.
# pydantic-settings merges .env file values with actual environment variables,
# with real env vars taking precedence over the .env file.
_ENV_CONFIG = SettingsConfigDict(
    env_file=".env", env_file_encoding="utf-8", extra="ignore"
)


class DatabaseSettings(BaseSettings):
    """Database infrastructure settings."""

    model_config = _ENV_CONFIG

    USER: str = Field(default="postgres", alias="POSTGRES_USER")
    PASSWORD: str = Field(default="secret_password", alias="POSTGRES_PASSWORD")
    HOST: str = Field(default="localhost", alias="POSTGRES_HOST")
    PORT: int = Field(default=5432, alias="POSTGRES_PORT")
    DB_NAME: str = Field(default="ai_taskflow_db", alias="POSTGRES_DB")

    @property
    def async_url(self) -> str:
        """Build the async connection URL required by SQLAlchemy with asyncpg."""
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB_NAME}"

    @property
    def sync_url(self) -> str:
        """Build the sync connection URL used by Alembic for running migrations."""
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB_NAME}"


class SecuritySettings(BaseSettings):
    """Encryption and authentication token settings."""

    model_config = _ENV_CONFIG

    # SecretStr hides the value in logs and prints to prevent accidental leaks
    SECRET_KEY: SecretStr = Field(
        default=SecretStr("super-secret-development-key-change-in-production")
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


class AISettings(BaseSettings):
    """AI provider keys and settings."""

    model_config = _ENV_CONFIG

    OPENAI_API_KEY: SecretStr | None = Field(default=None, alias="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: SecretStr | None = Field(default=None, alias="ANTHROPIC_API_KEY")


class Settings(BaseSettings):
    """Main application settings object (equivalent to IOptions in .NET)."""

    model_config = _ENV_CONFIG

    PROJECT_NAME: str = "AI Taskflow"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    # Instantiate settings sub-classes
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    ai: AISettings = Field(default_factory=AISettings)


# Global singleton imported by the rest of the application
settings = Settings()
