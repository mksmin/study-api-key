from pathlib import Path
from pydantic import PostgresDsn, BaseModel, ValidationError, Field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

PATH_PWD = Path(__file__).absolute().parent.parent.parent.parent


class SecretsConfig(BaseModel):
    key: str


class DatabaseConfig(BaseModel):
    scheme: str = 'postgresql'
    engine: str = "asyncpg"
    username: str
    password: str
    host: str = "localhost"
    port: int = 5432,
    path: str

    echo: bool = False,
    echo_pool: bool = False,
    pool_size: int = 50,
    max_overflow: int = 10,

    @property
    def url(self) -> str:
        try:
            url_path = MultiHostUrl.build(
                scheme=f'{self.scheme}+{self.engine}',
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.path
            )
        except ValidationError:
            raise ValueError("Invalid URL")
        return str(PostgresDsn(url_path))


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
        env_prefix="APP_CONFIG__",
    )

    db: DatabaseConfig
    run: RunConfig
    secret: SecretsConfig


settings = Settings()
