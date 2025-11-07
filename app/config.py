from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # credentials
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field("localhost", env="DB_HOST")
    db_port: int = Field(5432, env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")

    # additional pool settings 
    pool_pre_ping: bool = True
    pool_size: int = 10
    max_overflow: int = 20

    @property
    def database_url(self) -> str:
        """
        Return a standard SQLAlchemy URL for Postgres.
        """
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate once, read values from environment or .env
settings = Settings()
