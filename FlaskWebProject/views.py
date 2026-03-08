from flask import Blueprint, redirect, url_for, session, request
import msal
import logging
import os

bp = Blueprint('views', __name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TENANT_ID = os.environ.get("TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/auth/callback"
SCOPE = ["User.Read"]


@bp.route("/")
def home():
    return "Flask server is running correctly"


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
        logging.warning(f"Login attempt failed: {e}")
        return "Login failed"


@bp.route(REDIRECT_PATH)
def authorized():
    try:
        code = request.args.get("code")

        if not code:
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
            session["user"] = result.get("id_token_claims")
            return redirect(url_for("views.home"))

        return "Login failed"

    except Exception as e:
        logging.warning(f"Login failed: {e}")
        return "Login failed"
