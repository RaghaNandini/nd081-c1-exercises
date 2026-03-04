"""
This script runs the FlaskWebProject application using a development server.
"""

from os import environ
from FlaskWebProject import app

import config
from flask import Flask

app = Flask(__name__)
app.secret_key = config.SECRET_KEY  # use the secret key from config

# Example to check variables
print("SQL Server:", config.SQL_SERVER)
print("Blob Container:", config.BLOB_CONTAINER)
print("Client ID:", config.CLIENT_ID)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, ssl_context='adhoc')
