from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    # 1. Add this line so your code can read the database link from .env
    DATABASE_URL: str


    class Config:
        env_file = ".env"
        # 2. Add this line to prevent the "extra inputs" crash
        extra = "ignore" 

settings = Settings()