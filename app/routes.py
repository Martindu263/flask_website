from flask import render_template
from app import app

#2个路由
@app.route('/')
@app.route('/index')

#1个视图函数
def index():
	user = {'username': 'Developer'}
	return render_template('index.html', title='home', user=user)