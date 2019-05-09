import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_bootstrap import Bootstrap

from config import Config
from app.routes import git_webhook

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    """ Create, configure and return the Flask application """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    bootstrap.init_app(app)

    from app import models

    app.register_blueprint(git_webhook)

    return app
