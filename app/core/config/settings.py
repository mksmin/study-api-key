from pathlib import Path
from pydantic import PostgresDsn, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

PATH_PWD = Path(__file__).parent.parent.parent.parent

class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000
    log_level: str = "DEBUG"
    reload: bool = True
    workers: int = 1


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(PATH_PWD / ".env.template", PATH_PWD / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__"
    )

    run: RunConfig


settings = Settings()
