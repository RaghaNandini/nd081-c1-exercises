
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


from flask import Flask
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

    return app