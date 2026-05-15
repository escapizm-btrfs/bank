from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST : str
    DB_PORT : int
    DB_NAME : str
    DB_USER : str
    USER_PASSWORD : str

    SECRET_KEY : str
    ACCESS_TOKEN : int
    ALGORITHM : str
    
    class Config:
        env_file = ".env"

settings = Settings()