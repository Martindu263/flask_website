from flask import render_template, flash, redirect, url_for, request, make_response, jsonify #make_response, jsonify测试
from app import app
from app.forms import LoginForm, PostForm, ResetPasswordForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from app import db
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required			#增加保护视图，不允许未登陆的函数登陆上面的装饰器
#1个视图函数
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.post.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('成功发送！')
		return redirect(url_for('index'))
	posts = current_user.followed_posts().all()
	page = request.args.get('page', 1, type=int)
	posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('index', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
	return render_template("index.html", title='Home Page', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/explore')
@login_required
def explore():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()#表单实例化对象
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('用户名或密码错误！')
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

@app.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('请检查你的邮件来重置密码，有时密码重置邮件会出现在垃圾邮件中，请一并检查')
		return redirect(url_for('login'))
	return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('您的密码已经重置完成.')
		return redirect(url_for('login'))
	return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
	prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
	return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()

		flash('变更已经成功更改！')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='编辑个人信息', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('用户 {} 未找到。'.format(username))
		return redirect(url_for('index'))
	if user == current_user:
		flash('你不能自己关注自己。')
		return redirect(url_for('user', username=username))
	current_user.follow(user)
	db.session.commit()
	flash('你正在关注 {}!'.format(username))
	return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('用户 {} 未找到。'.format(username))
		return redirect(url_for('index'))
	if user == current_user:
		flash('你不能自己关注自己。')
		return redirect(url_for('user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash('你不再关注  {}.'.format(username))
	return redirect(url_for('user', username=username))


