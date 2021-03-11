from flask import Blueprint

_echarts = Blueprint('echarts', __name__)

from app.echarts import routes