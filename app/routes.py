from flask import render_template, flash, redirect, url_for, request, make_response, jsonify #make_response, jsonify测试
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from app import db
from app.forms import RegistrationForm
from flask_login import login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename #测试
import os#测试
import cv2#测试
import time#测试


@app.route('/')
@app.route('/index')
@login_required			#增加保护视图，不允许未登陆的函数登陆上面的装饰器
#1个视图函数
def index():

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
	return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()#表单实例化对象
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='登陆',form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, phone_number=form.phone_number.data, isteacher=form.isteacher.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('恭喜你，注册成功!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = [
		{'author':user, 'body':'Test post #1'},
		{'author':user, 'body':'Test post #2'}
	]
	return render_template('user.html', user=user, posts=posts)

################测试

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
@login_required
def upload():
	if request.method == 'POST':
		f = request.files['file']
		if not (f and allowed_file(f.filename)):
			return jsonify({"error": 1001, "msg": "1请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
		basepath = os.path.dirname(__file__)  # 当前文件所在路径
		upload_path = os.path.join(basepath, 'static/images/uploads', secure_filename(f.filename))
		f.save(upload_path)

		# 使用Opencv转换一下图片格式和名称
		img = cv2.imread(upload_path)
		pic_name = os.path.join(basepath, 'static/images/uploads', '%s.jpg' % (time.time()))
		cv2.imwrite(pic_name, img)

		return render_template('upload_ok.html',val1=time.time())

	return render_template('upload.html')





