import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_bootstrap import Bootstrap

from config import Config


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()


def create_app(config_class=Config):
    """ Create, configure and return the Flask application """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    bootstrap.init_app(app)

    from app import models
    from app.routes import git_webhook

    app.register_blueprint(git_webhook)

    return app
