"""
Routes and views for the flask application.
"""
'''
from datetime import datetime
from flask import render_template, flash, redirect, request, session, url_for
from werkzeug.urls import url_parse
from config import Config
from FlaskWebProject import app, db
from FlaskWebProject.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from FlaskWebProject.models import User, Post
import msal
import uuid

imageSourceUrl = 'https://'+ app.config['BLOB_ACCOUNT']  + '.blob.core.windows.net/' + app.config['BLOB_CONTAINER']  + '/'

@app.route('/')
@app.route('/home')
@login_required
def home():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.all()
    return render_template(
        'index.html',
        title='Home Page',
        posts=posts
    )

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm(request.form)
    if form.validate_on_submit():
        post = Post()
        post.save_changes(form, request.files['image_path'], current_user.id, new=True)
        return redirect(url_for('home'))
    return render_template(
        'post.html',
        title='Create Post',
        imageSource=imageSourceUrl,
        form=form
    )


@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get(int(id))
    form = PostForm(formdata=request.form, obj=post)
    if form.validate_on_submit():
        post.save_changes(form, request.files['image_path'], current_user.id)
        return redirect(url_for('home'))
    return render_template(
        'post.html',
        title='Edit Post',
        imageSource=imageSourceUrl,
        form=form
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session["state"])
    return render_template('login.html', title='Sign In', form=form, auth_url=auth_url)

@app.route(Config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("home"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        # TODO: Acquire a token from a built msal app, along with the appropriate redirect URI
        result = None
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        # Note: In a real app, we'd use the 'name' property from session["user"] below
        # Here, we'll use the admin username for anyone who is authenticated by MS
        user = User.query.filter_by(username="admin").first()
        login_user(user)
        _save_cache(cache)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    if session.get("user"): # Used MS Login
        # Wipe out user and its token cache from session
        session.clear()
        # Also logout from your tenant's web session
        return redirect(
            Config.AUTHORITY + "/oauth2/v2.0/logout" +
            "?post_logout_redirect_uri=" + url_for("login", _external=True))

    return redirect(url_for('login'))

def _load_cache():
    # TODO: Load the cache from `msal`, if it exists
    cache = None
    return cache

def _save_cache(cache):
    # TODO: Save the cache, if it has changed
    pass

def _build_msal_app(cache=None, authority=None):
    # TODO: Return a ConfidentialClientApplication
    return None

def _build_auth_url(authority=None, scopes=None, state=None):
    # TODO: Return the full Auth Request URL with appropriate Redirect URI
    return None
'''
"""
Routes and views for the flask application.
"""
'''from datetime import datetime
from flask import render_template, flash, redirect, request, session, url_for
from werkzeug.urls import url_parse
from config import Config
from FlaskWebProject import app, db
from FlaskWebProject.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from FlaskWebProject.models import User, Post
import msal
import uuid
from msal import SerializableTokenCache

# Blob Storage URL
imageSourceUrl = 'https://' + app.config['BLOB_ACCOUNT'] + '.blob.core.windows.net/' + app.config['BLOB_CONTAINER'] + '/'

# ------------------------
# Home Page
# ------------------------
@app.route('/')
@app.route('/home')
@login_required
def home():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.all()
    return render_template(
        'index.html',
        title='Home Page',
        posts=posts
    )

# ------------------------
# Create New Post
# ------------------------
@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm(request.form)
    if form.validate_on_submit():
        post = Post()
        post.save_changes(form, request.files['image_path'], current_user.id, new=True)
        return redirect(url_for('home'))
    return render_template(
        'post.html',
        title='Create Post',
        imageSource=imageSourceUrl,
        form=form
    )

# ------------------------
# Edit Post
# ------------------------
@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get(int(id))
    form = PostForm(formdata=request.form, obj=post)
    if form.validate_on_submit():
        post.save_changes(form, request.files['image_path'], current_user.id)
        return redirect(url_for('home'))
    return render_template(
        'post.html',
        title='Edit Post',
        imageSource=imageSourceUrl,
        form=form
    )

# ------------------------
# Login Route
# ------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            app.logger.warning(f"Invalid login attempt for username: {form.username.data}")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        app.logger.info(f"User {form.username.data} logged in successfully with local credentials")
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)

    # Microsoft OAuth2 login setup
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session["state"])
    return render_template('login.html', title='Sign In', form=form, auth_url=auth_url)

# ------------------------
# OAuth2 Redirect URI
# ------------------------
@app.route(Config.REDIRECT_PATH)  # Must match Entra ID redirect URI
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("home"))  # CSRF protection

    if "error" in request.args:
        return render_template("auth_error.html", result=request.args)

    if request.args.get('code'):
        cache = _load_cache()
        msal_app = _build_msal_app(cache=cache)
        result = msal_app.acquire_token_by_authorization_code(
            request.args['code'],
            scopes=Config.SCOPE,
            redirect_uri=url_for("authorized", _external=True)
        )

        if "access_token" in result:
            session["user"] = result.get("id_token_claims")
            app.logger.info(f"User {session['user'].get('preferred_username')} logged in successfully via MS login")
            user = User.query.filter_by(username="admin").first()  # Map to admin
            login_user(user)
            _save_cache(cache)
        else:
            app.logger.warning(f"MS login failed: {result.get('error_description')}")
            return render_template("auth_error.html", result=result)

    return redirect(url_for('home'))

# ------------------------
# Logout
# ------------------------
@app.route('/logout')
def logout():
    logout_user()
    if session.get("user"):
        session.clear()
        return redirect(
            Config.AUTHORITY + "/oauth2/v2.0/logout" +
            "?post_logout_redirect_uri=" + url_for("login", _external=True)
        )
    return redirect(url_for('login'))

# ------------------------
# MSAL Helper Functions
# ------------------------
def _load_cache():
    cache = SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        Config.CLIENT_ID,
        authority=authority or Config.AUTHORITY,
        client_credential=Config.CLIENT_SECRET,
        token_cache=cache
    )

def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes=scopes or Config.SCOPE,
        state=state,
        redirect_uri=url_for("authorized", _external=True)
    )
    '''
'''
from flask import Blueprint, redirect, url_for, session, request, render_template
import msal
import logging
import os
import config

def get_sql_server_info():
    print("Connecting to SQL Server:", config.SQL_SERVER)

def upload_to_blob(file_path, blob_name):
    from azure.storage.blob import BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER)
    with open(file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    print(f"{blob_name} uploaded successfully!")

bp = Blueprint('views', __name__)

# MSAL Configuration
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
AUTHORITY = "https://login.microsoftonline.com/common"
REDIRECT_PATH = "/getAToken"
SCOPE = ["User.Read"]  # Adjust if you need other permissions
SESSION_TYPE = "filesystem"

# -------------------
# Login Route
# -------------------
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
            redirect_uri=request.host_url.rstrip('/') + REDIRECT_PATH
        )
        return redirect(auth_url)
    except Exception as e:
        logging.warning(f"Login attempt failed: {e}")
        return "Login failed"

# -------------------
# Redirect URI Route
# -------------------
@bp.route(REDIRECT_PATH)
def authorized():
    try:
        code = request.args.get('code')
        if not code:
            logging.warning("No code returned in redirect")
            return "Login failed"

        msal_app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET
        )
        result = msal_app.acquire_token_by_authorization_code(
            code,
            scopes=SCOPE,
            redirect_uri=request.host_url.rstrip('/') + REDIRECT_PATH
        )
        if "access_token" in result:
            session["user"] = result.get("id_token_claims")
            logging.info(f"User {session['user'].get('preferred_username')} logged in successfully")
            return redirect(url_for('views.home'))
        else:
            logging.warning("Access token not found in result")
            return "Login failed"
    except Exception as e:
        logging.warning(f"Login failed: {e}")
        return "Login failed"

# -------------------
# Home Route
# -------------------
@bp.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", user=user)
    '''
    
from flask import Blueprint, redirect, url_for, session, request, render_template
import msal
import logging
import os
from FlaskWebProject import db
from FlaskWebProject.models import User, Post
from sqlalchemy import text

bp = Blueprint('views', __name__)

# MSAL Configuration
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
TENANT_ID = os.environ.get('TENANT_ID')
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/auth/callback"
SCOPE = ["User.Read"]  # Adjust if needed

# -------------------
# Home Route
# -------------------
@bp.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", user=user)

# -------------------
# Login Route
# -------------------
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
            redirect_uri=request.host_url.rstrip('/') + REDIRECT_PATH
        )
        return redirect(auth_url)
    except Exception as e:
        logging.warning(f"Login attempt failed: {e}")
        return "Login failed"

# -------------------
# Callback Route
# -------------------
@bp.route(REDIRECT_PATH)
def authorized():
    try:
        code = request.args.get('code')
        if not code:
            logging.warning("No code returned in redirect")
            return "Login failed"

        msal_app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET
        )
        result = msal_app.acquire_token_by_authorization_code(
            code,
            scopes=SCOPE,
            redirect_uri=request.host_url.rstrip('/') + REDIRECT_PATH
        )

        if "access_token" in result:
            session["user"] = result.get("id_token_claims")
            logging.info(f"User {session['user'].get('preferred_username')} logged in successfully")
            return redirect(url_for('views.home'))
        else:
            logging.warning("Access token not found in result")
            return "Login failed"
    except Exception as e:
        logging.warning(f"Login failed: {e}")
        return "Login failed"