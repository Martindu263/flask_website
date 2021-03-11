from flask import Blueprint

_errors = Blueprint('errors', __name__)

from app.errors import handlers