from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_location: str = "tasks.sqlite3"
    database_date_format: str = r"%Y-%m-%d"
    page_size: int = 10

    @property
    def database_connection_string(self):
        return f"sqlite:///{self.database_location}"


# instantiate a 'singleton'
settings = Settings()
