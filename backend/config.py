import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "databases")
    APP_DB = "app.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, APP_DB)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
