from flask import Blueprint

_main = Blueprint('main', __name__)

from app.main import routes