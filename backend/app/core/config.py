from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str="1908"
    ALGORITHM: str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int =30
    # 1. Add this line so your code can read the database link from .env
    DATABASE_URL: str="postgresql://postgres:1908@localhost:5432/productivity_os"


    class Config:
        env_file = ".env"
        # 2. Add this line to prevent the "extra inputs" crash
        extra = "ignore" 

settings = Settings()