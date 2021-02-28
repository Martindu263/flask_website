#从flask包中导入Flask类
from flask import Flask
#将Flask类的实例赋值给名为 app 的变量，这个实例成为app包的成员
app = Flask(__name__)

#从app包中导入模块routes
from app import routes	#此处在下面是为了避免循环引入
