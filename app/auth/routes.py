from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth import _auth
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Post
from app.auth.email import send_password_reset_email

import pymysql
import pandas as pd

@_auth.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()#表单实例化对象
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('用户名或密码错误！')
			return redirect(url_for('auth.login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('main.index')
		return redirect(next_page)
	#页面下半部分
	con = pymysql.connect(host='1.15.41.127', port=3306, db='education', user='lookup', passwd='lookup123456')
	list_score = [400, 450, 500, 550, 600, 650, 700, 750]
	a = 0
	b = 1
	sql_list1 = []
	sql_list2 = []
	while a<= 6:
		s = list_score[a]
		t = list_score[b]
		a = a + 1
		b = b + 1
		sql1 = 'select count(*) from like_1op_score_2020 where 总分 between %s and %s' % (s, t)
		sql_list1.append(sql1)
		sql2 = 'select count(*) from wenke_1op_score_2020 where 总分 between %s and %s' % (s, t)
		sql_list2.append(sql2)

	i = 0
	result1 = []
	while i <= len(sql_list1)-1:
		k1 = sql_list1[i]
		i += 1
		Kr1 = pd.read_sql(k1, con)
		Kw1 = Kr1.iat[0, 0]
		result1.append(Kw1)

	j = 0
	result2 = []
	while j <= len(sql_list2)-1:
		k2 = sql_list2[j]
		j += 1
		Kr2 = pd.read_sql(k2, con)
		Kw2 = Kr2.iat[0, 0]
		result2.append(Kw2)
	return render_template('auth/login.html', title='登陆',form=form,result1=result1, result2=result2)

@_auth.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@_auth.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, phone_number=form.phone_number.data, isteacher=form.isteacher.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('恭喜你，注册成功!')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', title='Register', form=form)

@_auth.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('请检查你的邮件来重置密码，有时密码重置邮件会出现在垃圾邮件中，请一并检查')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password_request.html', title='Reset Password', form=form)

@_auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('main.index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('您的密码已经重置完成.')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html', form=form)