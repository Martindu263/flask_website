from app import db, login
from sqlalchemy.sql import func
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from time import time
import jwt
from flask import current_app

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

followers = db.Table(#直接定义数据库表
	'followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),#关注者列，粉丝id
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))#被关注者列，大Vid
	)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	phone_number = db.Column(db.String(64), index=True, unique=True)
	isteacher = db.Column(db.Boolean, default=False)
	password_hash = db.Column(db.String(128))
	time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)

	followed = db.relationship(
		'User',
		secondary=followers,
		primaryjoin=(followers.c.follower_id==id),#上述id赋值为关系表的follower_id，和粉丝id链接
		secondaryjoin=(followers.c.followed_id==id),#上述id赋值给要关注的人，和大Vid链接
		backref=db.backref('followers', lazy='dynamic'),
		lazy='dynamic'
		)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id==user.id).count()>0

	def followed_posts(self):
			followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
			own = Post.query.filter_by(user_id=self.id)
			return followed.union(own).order_by(Post.timestamp.desc())

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},
			current_app.config['SECRET_KEY'], algorithm='HS256')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	#有哈希密码的表单添加下列方法
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location = db.Column(db.String(20))
	title = db.Column(db.String(80))
	body = db.Column(db.String(255))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)


