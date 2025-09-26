from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- Database (MySQL) ---
    DATABASE_DSN: str = "mysql+pymysql://root:shubha@mysql:3306/palm_minds"

    # --- Redis for chat memory ---
    REDIS_URL: str = "redis://redis:6379/0"

    # --- Vector DB (Qdrant) ---
    QDRANT_URL: str = "http://qdrant:6333"
    QDRANT_API_KEY: str | None = None  # <-- Add this

    # --- Embedding API Key (optional) ---
    EMBEDDING_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        extra = "allow"



settings = Settings()
