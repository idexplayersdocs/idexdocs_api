from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    MSSQL_USER: str
    MSSQL_HOSTNAME: str
    MSSQL_SA_PASSWORD: str
    APPLICATION_DB: str
    TOKEN_KEY: str
    STORAGE_ACCOUNT: str
