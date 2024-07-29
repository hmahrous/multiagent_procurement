# 1. (Most important, will overwrite everything) - environment variables
# 2. .env file in root folder of project
# 3. Default values

# "sqlalchemy_database_uri" is computed field that will create valid connection string

# See https://pydantic-docs.helpmanual.io/usage/settings/
# Note, complex types like lists are read as json-encoded strings.

from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL
_file_=''
PROJECT_DIR = Path(_file_).parent.parent.parent

class OpenAIConfig(BaseModel):
    openai_api_key: str = ""
    openai_endpoint: str = ""

class AppConfig(BaseModel):
    app_root: str = ""

class Settings(BaseSettings):
    open_ai_config: OpenAIConfig
    app_config: AppConfig

    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore