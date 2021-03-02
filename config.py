import os

basedir = os.path.abspath(os.path.dirname(__file__))#获取当前.py文件的绝对路径

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'website.env'))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess.'
	
	#数据库
	SQLALCHEMY_DATABASE_URI = 'mysql://root:yezizhu789@localhost/website'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	POSTS_PER_PAGE = 10
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
	MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', 'on', '1']
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')