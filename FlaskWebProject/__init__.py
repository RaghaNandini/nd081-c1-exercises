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
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Azure SQL
    app.config['SQL_SERVER'] = os.environ.get('SQL_SERVER')
    app.config['SQL_DATABASE'] = os.environ.get('SQL_DATABASE')
    app.config['SQL_USER_NAME'] = os.environ.get('SQL_USER')
    app.config['SQL_PASSWORD'] = os.environ.get('SQL_PASSWORD')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mssql+pyodbc://{app.config['SQL_USER_NAME']}:{app.config['SQL_PASSWORD']}"
        f"@{app.config['SQL_SERVER']}:1433/{app.config['SQL_DATABASE']}"
        "?driver=ODBC+Driver+18+for+SQL+Server"
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Initialize extensions
    db.init_app(app)
    login.init_app(app)

    # Register routes
    from FlaskWebProject.views import bp
    app.register_blueprint(bp)

    return app
