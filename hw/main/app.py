from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

import datetime

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from .routes import register_routes

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app
