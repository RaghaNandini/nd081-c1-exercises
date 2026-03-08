import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from FlaskWebProject import config

db = SQLAlchemy()
login = LoginManager()

def create_app():
    app = Flask(__name__)

    # Secret key
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', config.SECRET_KEY)

    # Azure SQL configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mssql+pyodbc://{config.SQL_USER_NAME}:{config.SQL_PASSWORD}"
        f"@{config.SQL_SERVER}:1433/{config.SQL_DATABASE}"
        "?driver=ODBC+Driver+18+for+SQL+Server"
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Logging
    logging.basicConfig(level=logging.INFO)

    # Initialize extensions
    db.init_app(app)
    login.init_app(app)

    # Register routes
    from FlaskWebProject.views import bp
    app.register_blueprint(bp)

    return app
