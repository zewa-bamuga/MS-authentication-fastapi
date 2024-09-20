import secrets
from typing import Any

from passlib.context import CryptContext
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    prefix: str = Field(default="/api")
    cors_origins: list[str] = Field(default=["http://localhost:3000"])
    show_docs: bool = Field(default=True)
    auth_uri: str = Field(default="/api/v1/users/authentication/oauth")
    model_config = SettingsConfigDict(env_prefix="API_")


class SecuritySettings(BaseSettings):
    pwd_context: CryptContext = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
        bcrypt__rounds=10,
    )
    secret_key: str = Field(default=secrets.token_urlsafe(32))
    private_key: str = Field(default=..., description="Private RSA key")
    public_key: str = Field(default=..., description="Public RSA key")

    access_expiration_min: int = Field(default=15)
    refresh_expiration_min: int = Field(default=60 * 24 * 7)

    model_config = SettingsConfigDict(env_prefix="SECURITY_")


class SentrySettings(BaseSettings):
    dsn: str | None = Field(default=None)
    traces_sample_rate: float = Field(default=0.2)
    env_name: str = Field(default="dev")

    @field_validator("dsn", mode="before")
    @classmethod
    def sentry_dsn_can_be_blank(cls, v: str) -> str | None:
        if v is None or len(v) == 0:
            return None
        return v

    model_config = SettingsConfigDict(env_prefix="SENTRY_")


class DatabaseSettings(BaseSettings):
    dsn: str = Field(default=...)
    model_config = SettingsConfigDict(env_prefix="DB_")


class MessageQueueSettings(BaseSettings):
    broker_uri: str | None = Field(default=None)
    model_config = SettingsConfigDict(env_prefix="MQ_")


class TasksSettings(BaseSettings):
    params: dict[str, Any] = {"activate_user": {"time_limit": 7200}}
    schedules: list[dict[str, Any]] = []
    model_config = SettingsConfigDict(env_prefix="TASKS_")


class Settings(BaseSettings):
    api: ApiSettings = ApiSettings()
    security: SecuritySettings = SecuritySettings()
    sentry: SentrySettings = SentrySettings()
    db: DatabaseSettings = DatabaseSettings()
    mq: MessageQueueSettings = MessageQueueSettings()
    tasks: TasksSettings = TasksSettings()
