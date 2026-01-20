from functools import lru_cache
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    
    is_development: bool = True

    user_principal_name_dev: str = "johndoe@hotmail.com"

    app_name: str = "LoreAgentApire"

    azure_openai_endpoint: str

    azure_openai_version: str

    openai_chat_deployment_name: str

config = Config()