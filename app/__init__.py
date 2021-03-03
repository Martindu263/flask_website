#从flask包中导入Flask类
from flask import Flask
from config import Config
#将Flask类的实例赋值给名为 app 的变量，这个实例成为app包的成员

from flask_sqlalchemy import SQLAlchemy#从包中导入类
from flask_migrate import Migrate
import pymysql 
from flask_login import LoginManager	#增加登陆
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from datetime import timedelta#测试


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)#数据库对象
migrate = Migrate(app, db)#迁移引擎对象
pymysql.install_as_MySQLdb()
login = LoginManager(app)
login.login_view = 'login'
login.login_message = u'请登陆'
app.send_file_max_age_default = timedelta(seconds=1) #测试
mail = Mail(app)
bootstrap = Bootstrap(app)

#从app包中导入模块routes
from app import routes, models, errors	#此处在下面是为了避免循环引入
