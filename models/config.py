import os
from pydantic import BaseSettings 
class Settings(BaseSettings):
   
    DATABASE_MIGRATION_URI : str=os.getenv('DATABASE_MIGRATION_URI') 
    DATABASE_ASYNC_URI : str=os.getenv("DATABASE_ASYNC_URI")
    SECRET_KEY : str = os.getenv("SECRET_KEY")
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()