
"""
The flask application package.
"""
'''
import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
#TOD O: Add any logging levels and handlers with app.logger
Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

import FlaskWebProject.views
'''

"""
The flask application package.
"""
'''
import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

# ------------------------
# Flask App Setup
# ------------------------
app = Flask(__name__)
app.config.from_object(Config)

# ------------------------
# Logging Setup
# ------------------------
logging.basicConfig(
    level=logging.INFO,  # INFO will show successes, WARNING will show failed logins
    format='%(asctime)s - %(levelname)s - %(message)s'
)
app.logger = logging.getLogger(__name__)

# ------------------------
# Session, DB, Login
# ------------------------
Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

# ------------------------
# Import views
# ------------------------
import FlaskWebProject.views
'''

'''
from flask import Flask
from . import views
import logging
import os

def create_app():
    app = Flask(__name__)

    # -------------------
    # App Configuration
    # -------------------
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
    app.config['BLOB_ACCOUNT'] = os.environ.get('BLOB_ACCOUNT')
    app.config['BLOB_STORAGE_KEY'] = os.environ.get('BLOB_STORAGE_KEY')
    app.config['BLOB_CONTAINER'] = os.environ.get('BLOB_CONTAINER')
    app.config['BLOB_CONNECTION_STRING'] = os.environ.get('BLOB_CONNECTION_STRING')
    app.config['SQL_SERVER'] = os.environ.get('SQL_SERVER')
    app.config['SQL_DATABASE'] = os.environ.get('SQL_DATABASE')
    app.config['SQL_USER_NAME'] = os.environ.get('SQL_USER_NAME')
    app.config['SQL_PASSWORD'] = os.environ.get('SQL_PASSWORD')
    app.config['CLIENT_ID'] = os.environ.get('CLIENT_ID')
    app.config['CLIENT_SECRET'] = os.environ.get('CLIENT_SECRET')
    # Load configuration from environment variables
    app.config.from_object('config.Config')  # Loads your config.py

    # -------------------
    # Logging Setup
    # -------------------
    logging.basicConfig(
        level=logging.INFO,
        filename='app.log',
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Import routes
    from . import views
    app.register_blueprint(views.bp)

    return app'''
'''
# FlaskWebProject/__init__.py
from flask import Flask
import logging
import os

def create_app():
    # Create Flask app
    app = Flask(__name__)

    # -------------------
    # Load configuration from environment variables and config.py
    # -------------------
    app.config.from_object('config.Config')  # Loads your config.py

    # Fallbacks (optional, in case env vars not set)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', app.config.get('SECRET_KEY', 'your-secret-key'))
    app.config['BLOB_ACCOUNT'] = os.environ.get('BLOB_ACCOUNT', app.config.get('BLOB_ACCOUNT'))
    app.config['BLOB_STORAGE_KEY'] = os.environ.get('BLOB_STORAGE_KEY', app.config.get('BLOB_STORAGE_KEY'))
    app.config['BLOB_CONTAINER'] = os.environ.get('BLOB_CONTAINER', app.config.get('BLOB_CONTAINER'))
    app.config['BLOB_CONNECTION_STRING'] = os.environ.get('BLOB_CONNECTION_STRING', app.config.get('BLOB_CONNECTION_STRING'))
    app.config['SQL_SERVER'] = os.environ.get('SQL_SERVER', app.config.get('SQL_SERVER'))
    app.config['SQL_DATABASE'] = os.environ.get('SQL_DATABASE', app.config.get('SQL_DATABASE'))
    app.config['SQL_USER_NAME'] = os.environ.get('SQL_USER', app.config.get('SQL_USER_NAME'))
    app.config['SQL_PASSWORD'] = os.environ.get('SQL_PASSWORD', app.config.get('SQL_PASSWORD'))
    app.config['CLIENT_ID'] = os.environ.get('CLIENT_ID', app.config.get('CLIENT_ID'))
    app.config['CLIENT_SECRET'] = os.environ.get('CLIENT_SECRET', app.config.get('CLIENT_SECRET'))

    # -------------------
    # Logging Setup
    # -------------------
    logging.basicConfig(
        level=logging.INFO,
        filename='app.log',
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # -------------------
    # Register Blueprints
    # -------------------
    from . import views
    app.register_blueprint(views.bp)

    return app'''
    
    
import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

# Initialize DB and Login globally
db = SQLAlchemy()
login = LoginManager()

def create_app():
    app = Flask(__name__)

    # -------------------
    # App Configuration
    # -------------------
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
    app.config['BLOB_ACCOUNT'] = os.environ.get('BLOB_ACCOUNT')
    app.config['BLOB_STORAGE_KEY'] = os.environ.get('BLOB_ACCOUNT_KEY')
    app.config['BLOB_CONTAINER'] = os.environ.get('BLOB_CONTAINER')
    app.config['BLOB_CONNECTION_STRING'] = os.environ.get('BLOB_CONNECTION_STRING')
    app.config['SQL_SERVER'] = os.environ.get('SQL_SERVER')
    app.config['SQL_DATABASE'] = os.environ.get('SQL_DATABASE')
    app.config['SQL_USER_NAME'] = os.environ.get('SQL_USER')
    app.config['SQL_PASSWORD'] = os.environ.get('SQL_PASSWORD')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mssql+pyodbc://{app.config['SQL_USER_NAME']}:{app.config['SQL_PASSWORD']}"
        f"@{app.config['SQL_SERVER']}:1433/{app.config['SQL_DATABASE']}?driver=ODBC+Driver+18+for+SQL+Server"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['CLIENT_ID'] = os.environ.get('CLIENT_ID')
    app.config['CLIENT_SECRET'] = os.environ.get('CLIENT_SECRET')
    app.config['TENANT_ID'] = os.environ.get('TENANT_ID')
    app.config['REDIRECT_URI'] = os.environ.get('REDIRECT_URI')

    # -------------------
    # Logging Setup
    # -------------------
    logging.basicConfig(
        level=logging.INFO,
        filename='app.log',
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # -------------------
    # Initialize extensions
    # -------------------
    db.init_app(app)
    login.init_app(app)
    Session(app)

    # Import and register routes
    from . import views
    app.register_blueprint(views.bp)

    return app