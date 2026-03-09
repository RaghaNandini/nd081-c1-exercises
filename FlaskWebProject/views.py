from flask import Blueprint, render_template, redirect, url_for, session, request
import msal
import logging
import os
from FlaskWebProject import db
from sqlalchemy import text

bp = Blueprint('views', __name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TENANT_ID = os.environ.get("TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/getAToken"
SCOPE = ["User.Read"]


# -------------------------------
# HOME PAGE
# -------------------------------
@bp.route("/")
def home():
    try:
        conn = db.engine.connect()

        users = conn.execute(text("SELECT * FROM users")).fetchall()
        posts = conn.execute(text("SELECT * FROM posts")).fetchall()

        conn.close()

    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        users = []
        posts = []

    return render_template(
        "index.html",
        users=users,
        posts=posts,
        title="Article CMS"
    )


# -------------------------------
# CREATE NEW POST PAGE
# -------------------------------
@bp.route("/new_post", methods=["GET", "POST"])
def new_post():

    try:
        conn = db.engine.connect()

        users = conn.execute(text("SELECT * FROM users")).fetchall()

        if request.method == "POST":

            title = request.form.get("title")
            user_id = request.form.get("user_id")
            body = request.form.get("body")

            # get username from users table
            user_query = text("SELECT username FROM users WHERE id=:id")
            user = conn.execute(user_query, {"id": user_id}).fetchone()

            author = user.username if user else "Unknown"

            insert_query = text("""
                INSERT INTO posts (title, author, body, user_id)
                VALUES (:title, :author, :body, :user_id)
            """)

            conn.execute(insert_query, {
                "title": title,
                "author": author,
                "body": body,
                "user_id": user_id
            })

            conn.commit()
            conn.close()

            return redirect(url_for("views.home"))

        conn.close()

        return render_template(
            "post.html",
            title="Create New Post",
            post=None,
            users=users
        )

    except Exception as e:
        logging.error(f"Post creation error: {str(e)}")
        return "Error creating post"


# -------------------------------
# LOGIN WITH MICROSOFT
# -------------------------------
@bp.route("/login")
def login():

    try:
        msal_app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET
        )

        auth_url = msal_app.get_authorization_request_url(
            scopes=SCOPE,
            redirect_uri=request.host_url.rstrip("/") + REDIRECT_PATH
        )

        return redirect(auth_url)

    except Exception as e:
        logging.error(f"Login redirect error: {str(e)}")
        return "Login failed"


# -------------------------------
# AUTH CALLBACK
# -------------------------------
@bp.route(REDIRECT_PATH)
def authorized():

    try:
        code = request.args.get("code")

        if not code:
            logging.warning("Invalid login attempt")
            return "Login failed"

        msal_app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET
        )

        result = msal_app.acquire_token_by_authorization_code(
            code,
            scopes=SCOPE,
            redirect_uri=request.host_url.rstrip("/") + REDIRECT_PATH
        )

        if "access_token" in result:

            user = result.get("id_token_claims")
            session["user"] = user

            logging.info(
                f"{user.get('preferred_username')} logged in successfully"
            )

            return redirect(url_for("views.home"))

        else:
            logging.warning("Invalid login attempt")
            return "Login failed"

    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return "Login failed"


# -------------------------------
# LOGOUT
# -------------------------------
@bp.route("/logout")
def logout():

    try:
        session.clear()
        return redirect(url_for("views.home"))

    except Exception as e:
        logging.error(f"Logout error: {str(e)}")
        return redirect(url_for("views.home"))