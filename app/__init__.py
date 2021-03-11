import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
#从flask包中导入Flask类
from flask import Flask, request
from config import Config
#将Flask类的实例赋值给名为 app 的变量，这个实例成为app包的成员

from flask_sqlalchemy import SQLAlchemy#从包中导入类
from flask_migrate import Migrate
import pymysql 
from flask_login import LoginManager	#增加登陆
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from datetime import timedelta#测试
from flask_moment import Moment
from config import Config
from flask import current_app

moment = Moment()
db = SQLAlchemy()#数据库对象
migrate = Migrate()#迁移引擎对象
pymysql.install_as_MySQLdb()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = u'请登陆'
mail = Mail()
bootstrap = Bootstrap()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)
	mail.init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)

	from app.errors import _errors as errors_bp
	app.register_blueprint(errors_bp)

	from app.auth import _auth as auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')

	from app.main import _main as main_bp
	app.register_blueprint(main_bp)

	from app.echarts import _echarts as echarts_bp
	app.register_blueprint(echarts_bp)

	return app



#从app包中导入模块routes
from app import models	#此处在下面是为了避免循环引入
