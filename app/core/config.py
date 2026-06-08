from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_version: str
    environment: str
    
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    
    redis_host: str 
    redis_port: int 
    cache_ttl: int 

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()