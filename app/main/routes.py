from flask import render_template, flash, redirect, url_for, request, current_app
from app.main.forms import PostForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required#
from app.models import User, Post#
from app import db#
from werkzeug.urls import url_parse#
from datetime import datetime
from datetime import datetime
from app.main import _main

@_main.before_app_request
def before_app_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@_main.route('/', methods=['GET', 'POST'])
@_main.route('/index', methods=['GET', 'POST'])
@login_required			#增加保护视图，不允许未登陆的函数登陆上面的装饰器
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.post.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('成功发送！')
		return redirect(url_for('main.index'))
	posts = current_user.followed_posts().all()
	page = request.args.get('page', 1, type=int)
	posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
	return render_template("index.html", title='Home Page', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)

@_main.route('/explore')
@login_required
def explore():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


@_main.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None
	return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@_main.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()

		flash('变更已经成功更改！')
		return redirect(url_for('main.edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='编辑个人信息', form=form)

@_main.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('用户 {} 未找到。'.format(username))
		return redirect(url_for('main.index'))
	if user == current_user:
		flash('你不能自己关注自己。')
		return redirect(url_for('main.user', username=username))
	current_user.follow(user)
	db.session.commit()
	flash('你正在关注 {}!'.format(username))
	return redirect(url_for('main.user', username=username))

@_main.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('用户 {} 未找到。'.format(username))
		return redirect(url_for('main.index'))
	if user == current_user:
		flash('你不能自己关注自己。')
		return redirect(url_for('main.user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash('你不再关注  {}.'.format(username))
	return redirect(url_for('user', username=username))


