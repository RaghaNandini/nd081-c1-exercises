from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from . import config

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = config.SECRET_KEY

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mssql+pyodbc://{config.SQL_USER_NAME}:{config.SQL_PASSWORD}"
        f"@{config.SQL_SERVER}:1433/{config.SQL_DATABASE}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .views import bp
    app.register_blueprint(bp)

    return app