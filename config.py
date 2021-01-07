from pydantic import BaseSettings
from dotenv import load_dotenv
import os

# load_dotenv()

# settings.py
SECRET_KEY = os.getenv("EMAIL")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

class Settings(BaseSettings):
    SECRET_KEY : str = os.environ.get('SECRET_KEY') or "secret"
    MAIL_USERNAME : str = os.environ.get('MAIL_USERNAME') or "a9f521690f65a4"
    MAIL_PASSWORD : str = os.environ.get('MAIL_PASSWORD') or "11480b2eec8121"
    MAIL_FROM : str = os.environ.get('MAIL_FROM') or "elisegb-49cabc@inbox.mailtrap.io"
    MAIL_PORT : int = os.environ.get('MAIL_PORT') or 2525
    MAIL_SERVER : str = os.environ.get('MAIL_SERVER') or "smtp.mailtrap.io"
    MAIL_TLS : bool = os.environ.get('MAIL_TLS') or False
    MAIL_SSL : bool = os.environ.get('MAIL_SSL') or False

    class Config:
        title = 'Base Settings'

