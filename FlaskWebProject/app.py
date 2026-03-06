import os
import logging
import urllib
import uuid

from flask import Flask, jsonify, render_template, session, redirect, request, url_for
from sqlalchemy import create_engine, text
import msal
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Azure SQL Database configuration
SQL_SERVER = "cms-sql-server.database.windows.net"
SQL_DATABASE = "cms"
SQL_USER = "cmsadmin"
SQL_PASSWORD = "Nandini@1"

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=30;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", echo=False)


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


@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())

    auth_url = _build_msal_app().get_authorization_request_url(
        config.SCOPE,
        state=session["state"],
        redirect_uri=url_for("authorized", _external=True)
    )

    return redirect(auth_url)


@app.route(config.REDIRECT_PATH)
def authorized():

    if request.args.get("state") != session.get("state"):
        logging.warning("Invalid login attempt")
        return redirect(url_for("index"))

    if "error" in request.args:
        logging.warning("Login error: %s", request.args.get("error_description"))
        return "Login error"

    if "code" in request.args:

        result = _build_msal_app().acquire_token_by_authorization_code(
            request.args["code"],
            scopes=config.SCOPE,
            redirect_uri=url_for("authorized", _external=True)
        )

        if "access_token" in result:

            session["user"] = result.get("id_token_claims")

            username = session["user"].get("preferred_username") or session["user"].get("name")

            logging.info(f"{username} logged in successfully")

            with engine.begin() as conn:

                user_row = conn.execute(
                    text("SELECT id FROM USERS WHERE username=:username"),
                    {"username": username}
                ).mappings().first()

                if user_row:
                    session["user_id"] = user_row["id"]
                else:

                    inserted_id = conn.execute(
                        text("INSERT INTO USERS (username) OUTPUT INSERTED.id VALUES (:username)"),
                        {"username": username}
                    ).scalar()

                    session["user_id"] = inserted_id

        else:
            logging.warning("Invalid login attempt")

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    logging.info("User logged out")
    return redirect("/")


# -------------------------
# Home Page
# -------------------------
@app.route("/")
@app.route("/index")
def index():

    with engine.connect() as conn:

        users_result = conn.execute(text("SELECT * FROM USERS")).mappings()
        users = [dict(u) for u in users_result]

        posts_result = conn.execute(text("SELECT * FROM POSTS")).mappings()
        posts = [dict(p) for p in posts_result]

    return render_template("index.html", users=users, posts=posts)


# -------------------------
# API Routes
# -------------------------
@app.route("/users")
def get_users():

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM USERS"))
        users = [dict(row) for row in result.mappings()]

    return jsonify(users)


@app.route("/posts")
def get_posts():

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM POSTS"))
        posts = [dict(row) for row in result.mappings()]

    return jsonify(posts)


# -------------------------
# Create Post
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

        image_path = None

        image_file = request.files.get("image_path")

        if image_file and image_file.filename != "":
            image_path = f"static/uploads/{image_file.filename}"

            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            image_file.save(image_path)

        if not user_id:
            return "Error: Must select an author", 403

        with engine.begin() as conn:

            user_row = conn.execute(
                text("SELECT username FROM USERS WHERE id=:id"),
                {"id": user_id}
            ).mappings().first()

            author_name = user_row["username"] if user_row else "Unknown"

            conn.execute(
                text(
                    "INSERT INTO POSTS (title, body, image_path, user_id, author) "
                    "VALUES (:title, :body, :image_path, :user_id, :author)"
                ),
                {
                    "title": title,
                    "body": body,
                    "image_path": image_path,
                    "user_id": user_id,
                    "author": author_name
                }
            )

        logging.info(f"New post created: {title}")

        return redirect("/")

    return render_template("post.html", title="Create New Post", users=users)


# -------------------------
# Edit Post
# -------------------------
@app.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):

    with engine.connect() as conn:

        post_data = conn.execute(
            text("SELECT * FROM POSTS WHERE id=:id"),
            {"id": id}
        ).mappings().first()

    if not post_data:
        return "Post not found", 404

    with engine.connect() as conn:

        users_result = conn.execute(text("SELECT * FROM USERS")).mappings()
        users = [dict(u) for u in users_result]

    if request.method == "POST":

        title = request.form.get("title")
        body = request.form.get("body")
        user_id = request.form.get("user_id")

        image_path = post_data["image_path"]

        image_file = request.files.get("image_path")

        if image_file and image_file.filename != "":
            image_path = f"static/uploads/{image_file.filename}"

            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            image_file.save(image_path)

        with engine.begin() as conn:

            user_row = conn.execute(
                text("SELECT username FROM USERS WHERE id=:id"),
                {"id": user_id}
            ).mappings().first()

            author_name = user_row["username"] if user_row else "Unknown"

            conn.execute(
                text(
                    "UPDATE POSTS SET title=:title, body=:body, image_path=:image_path, "
                    "user_id=:user_id, author=:author WHERE id=:id"
                ),
                {
                    "title": title,
                    "body": body,
                    "image_path": image_path,
                    "user_id": user_id,
                    "author": author_name,
                    "id": id
                }
            )

        logging.info(f"Post updated: {title}")

        return redirect("/")

    return render_template("post.html", title="Edit Post", post=post_data, users=users)


# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)