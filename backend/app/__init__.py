from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__, static_url_path="", static_folder="/../frontend/dist")
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

from app import routes, models