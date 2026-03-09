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
    conn = db.engine.connect()

    users = conn.execute(text("SELECT * FROM users")).fetchall()
    posts = conn.execute(text("SELECT * FROM posts")).fetchall()

    return render_template(
        "index.html",
        users=users,
        posts=posts,
        title="Article CMS"
    )


# -------------------------------
# LOGIN WITH MICROSOFT
# -------------------------------
@bp.route("/login")
def login():

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


# -------------------------------
# AUTH CALLBACK
# -------------------------------
@bp.route(REDIRECT_PATH)
def authorized():

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

        logging.info(f"{user.get('preferred_username')} logged in successfully")

        return redirect(url_for("views.home"))

    else:
        logging.warning("Invalid login attempt")
        return "Login failed"


# -------------------------------
# LOGOUT
# -------------------------------
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("views.home"))
