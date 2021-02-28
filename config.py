import os

basedir = os.path.abspath(os.path.dirname(__file__))#获取当前.py文件的绝对路径

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess.'
	
	#数据库
	SQLALCHEMY_DATABASE_URI = 'mysql://root:yezizhu789@localhost/website'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
