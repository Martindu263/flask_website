from flask import Blueprint

bp = Blueprint('echarts', __name__)

from app.echarts import routes