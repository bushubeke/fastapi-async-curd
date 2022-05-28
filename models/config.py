import os
from pydantic import BaseSettings 


class Settings(BaseSettings):
    #email settings to be filled
    # SMTP_TLS: bool = True
    # SMTP_PORT: Optional[int] = None
    # SMTP_HOST: Optional[str] = None
    # SMTP_USER: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None
    # EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    # EMAILS_FROM_NAME: Optional[str] = None

   
    DATABASE_MIGRATION_URI =os.getenv('DATABASE_MIGRATION_URI') 
    DATABASE_ASYNC_URI=os.getenv("DATABASE_ASYNC_URI")
    class Config:
        case_sensitive = True


settings = Settings()