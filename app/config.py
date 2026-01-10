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
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: Optional[str] = None
    
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
