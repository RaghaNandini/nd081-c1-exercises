import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from FlaskWebProject import config

db = SQLAlchemy()
login = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = config.SECRET_KEY

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mssql+pyodbc://{config.SQL_USER_NAME}:{config.SQL_PASSWORD}"
        f"@{config.SQL_SERVER}:1433/{config.SQL_DATABASE}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    logging.basicConfig(level=logging.INFO)

    db.init_app(app)
    login.init_app(app)

    from FlaskWebProject.views import bp
    app.register_blueprint(bp)

    return app
