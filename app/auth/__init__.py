from flask import Blueprint

_auth = Blueprint('auth', __name__)

from app.auth import routes