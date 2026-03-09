import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from FlaskWebProject import config

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = config.SECRET_KEY

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mssql+pyodbc://{config.SQL_USER_NAME}:{config.SQL_PASSWORD}"
        f"@{config.SQL_SERVER}:1433/{config.SQL_DATABASE}"
        "?driver=ODBC+Driver+18+for+SQL+Server"
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    logging.basicConfig(level=logging.INFO)

    db.init_app(app)

    from FlaskWebProject.views import bp
    app.register_blueprint(bp)

    return app
