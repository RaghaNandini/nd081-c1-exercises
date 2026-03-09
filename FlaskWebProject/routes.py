from flask import Blueprint

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return "Flask server is running correctly"