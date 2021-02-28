from flask import render_template
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
#1个视图函数
def index():
	user = {'username': 'Monkey'}

	posts = [
		{
			'author': {'username': 'john'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'susan'},
			'body': 'Beautiful day in USA!'
		}
		]
	return render_template('index.html', user=user, posts=posts)

@app.route('/login')
def login():
	form = LoginForm()#表单实例化对象
	return render_template('login.html', title='Sign In', form=form)
