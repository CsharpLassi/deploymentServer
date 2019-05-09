import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
from .webhooks import webhook

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """ Create, configure and return the Flask application """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(db)
    migrate.init_app(db, db)

    from app import models

    app.register_blueprint(webhook)

    return app
