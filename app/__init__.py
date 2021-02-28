#从flask包中导入Flask类
from flask import Flask
from config import Config
#将Flask类的实例赋值给名为 app 的变量，这个实例成为app包的成员

from flask_sqlalchemy import SQLAlchemy#从包中导入类
from flask_migrate import Migrate
import pymysql 

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)#数据库对象
migrate = Migrate(app, db)#迁移引擎对象
pymysql.install_as_MySQLdb()

#从app包中导入模块routes
from app import routes, models	#此处在下面是为了避免循环引入
