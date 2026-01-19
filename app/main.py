from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routers import auth, contracts
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TrustLayer AI API",
    description="AI-powered contract analysis and trust verification",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        settings.FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Include routers
app.include_router(auth.router)
app.include_router(contracts.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TrustLayer AI API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "trustlayer-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )

