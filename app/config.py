from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_migrate import Migrate
from flask_login import LoginManager
from os import getenv, path


basedir = path.abspath(path.dirname(__file__))
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
admin = Admin()


def create_app():
    app = Flask(__name__)
    app.secret_key = getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URL", "sqlite://")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    return app
