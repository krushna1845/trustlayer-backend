from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./trustlayer.db"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI APIs
    ANTHROPIC_API_KEY: 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
    OPENAI_API_KEY: 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
    
    # CORS
    FRONTEND_URL: str = "https://trustlayarai.vercel.app"
    
    # Server
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
