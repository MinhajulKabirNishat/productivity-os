from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # These must match the names in your .env file
    SECRET_KEY: str = "your_secret_key_here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ADD THIS LINE BELOW - it fixes the current crash
    DATABASE_URL: str = "sqlite:///./test.db" 

    class Config:
        env_file = ".env"
        # This prevents the "extra inputs" error if you have other stuff in .env
        extra = "ignore" 

settings = Settings()