import os


class Config:
    DB_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "databases")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'app.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-key-@JHh#*&##98h8sdmbq9h9E7FG5&hfsdlf)'
