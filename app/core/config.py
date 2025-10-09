# import os
# from dotenv import load_dotenv
# from pydantic import BaseSettings

# load_dotenv()

# class Settings(BaseSettings):
#     SUPABASE_URL: str = os.getenv("SUPABASE_URL")
#     SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
#     PROJECT_NAME: str = "Vidriados API"
#     VERSION: str = "0.1.0"

# settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str

    class Config:
        env_file = ".env"

# Instancia global de configuración
settings = Settings()
