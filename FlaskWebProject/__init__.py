from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config
import urllib
import logging

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    # Secret key
    app.config["SECRET_KEY"] = config.SECRET_KEY or "dev-secret-key"

    # ---------------------------
    # LOGGING CONFIGURATION
    # ---------------------------
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s : %(message)s"
    )

    # ---------------------------
    # DATABASE CONNECTION
    # ---------------------------
    params = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={config.SQL_SERVER};"
        f"DATABASE={config.SQL_DATABASE};"
        f"UID={config.SQL_USER_NAME};"
        f"PWD={config.SQL_PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # ---------------------------
    # REGISTER ROUTES
    # ---------------------------
    from .views import bp
    app.register_blueprint(bp)

    return app
