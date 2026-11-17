from pydantic_settings import BaseSettings , SettingsConfigDict

# BaseSettings provides a class that reads settings from environment variables and can validate their types.
# SettingsConfigDict configures where settings come from.

class Settings(BaseSettings):
    database_url: str 
    # debug: bool = False
    model_config = SettingsConfigDict(env_file =".env")
# Pydantic reads values and converts them to the declared types where possible. For example, it can parse APP_DEBUG=true as True when the prefix is configured.

# So this syntax configures how settings are loaded, while the class fields define which settings your app expects.

settings = Settings()
