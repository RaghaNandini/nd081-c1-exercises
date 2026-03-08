import os
import logging
import urllib
import uuid

from flask import Flask, jsonify, render_template, session, redirect, request, url_for
from sqlalchemy import create_engine, text
import msal
from azure.storage.blob import BlobServiceClient
from FlaskWebProject import config


# -------------------------
# Logging Configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -------------------------
# Flask App
# -------------------------
app = Flask(__name__)
app.secret_key = config.SECRET_KEY


# -------------------------
# Azure SQL Database
# -------------------------
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

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


# -------------------------
# Azure Blob Storage
# -------------------------
blob_service_client = BlobServiceClient.from_connection_string(
    config.BLOB_CONNECTION_STRING
)

blob_container_client = blob_service_client.get_container_client(
    config.BLOB_CONTAINER
)


# -------------------------
# MSAL Authentication
# -------------------------
def _build_msal_app(cache=None, authority=None):

    return msal.ConfidentialClientApplication(
        config.CLIENT_ID,
        authority=authority or config.AUTHORITY,
        client_credential=config.CLIENT_SECRET,
        token_cache=cache,
    )


# -------------------------
# LOGIN
# -------------------------
@app.route("/login")
def login():

    session["state"] = str(uuid.uuid4())

    auth_url = _build_msal_app().get_authorization_request_url(
        config.SCOPE,
        state=session["state"],
        redirect_uri=url_for("authorized", _external=True)
    )

    return redirect(auth_url)


# -------------------------
# Microsoft Callback
# -------------------------
@app.route(config.REDIRECT_PATH)
def authorized():

    if request.args.get("state") != session.get("state"):
        logging.warning("Invalid login attempt")
        return redirect(url_for("index"))

    if "error" in request.args:
        logging.warning("Login error")
        return redirect(url_for("index"))

    if "code" in request.args:

        result = _build_msal_app().acquire_token_by_authorization_code(
            request.args["code"],
            scopes=config.SCOPE,
            redirect_uri=url_for("authorized", _external=True)
        )

        if "access_token" in result:

            session["user"] = result.get("id_token_claims")

            username = (
                session["user"].get("preferred_username")
                or session["user"].get("name")
                or "admin"
            )

            logging.info(f"{username} logged in successfully")

        else:
            logging.warning("Invalid login attempt")

    return redirect(url_for("index"))


# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():

    user = session.get("user", {}).get("name", "User")

    logging.info(f"{user} logged out")

    session.clear()

    return redirect("/")


# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def index():

    try:

        with engine.connect() as conn:

            users_result = conn.execute(text("SELECT * FROM USERS")).mappings()
            users = [dict(u) for u in users_result]

            posts_result = conn.execute(text("SELECT * FROM POSTS")).mappings()
            posts = [dict(p) for p in posts_result]

        return render_template("index.html", users=users, posts=posts)

    except Exception as e:

        logging.error(f"Database error: {e}")

        return f"Database error: {e}", 500


# -------------------------
# CREATE POST
# -------------------------
@app.route("/new_post", methods=["GET", "POST"])
def new_post():

    with engine.connect() as conn:
        users_result = conn.execute(text("SELECT * FROM USERS")).mappings()
        users = [dict(u) for u in users_result]

    if request.method == "POST":

        title = request.form.get("title")
        body = request.form.get("body")
        user_id = request.form.get("user_id")

        image_file = request.files.get("image_path")

        image_url = None

        if image_file and image_file.filename != "":

            blob_client = blob_container_client.get_blob_client(image_file.filename)

            blob_client.upload_blob(image_file)

            image_url = blob_client.url

        with engine.begin() as conn:

            user_row = conn.execute(
                text("SELECT username FROM USERS WHERE id=:id"),
                {"id": user_id}
            ).mappings().first()

            author_name = user_row["username"]

            conn.execute(

                text(
                    "INSERT INTO POSTS (title, body, image_path, user_id, author) "
                    "VALUES (:title, :body, :image_path, :user_id, :author)"
                ),

                {
                    "title": title,
                    "body": body,
                    "image_path": image_url,
                    "user_id": user_id,
                    "author": author_name
                }

            )

        return redirect("/")

    return render_template("post.html", title="Create New Post", users=users)


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
