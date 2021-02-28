from app import db
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	phone_number = db.Column(db.String(64), index=True, unique=True)
	isteacher = db.Column(db.Boolean, default=False)
	password_hash = db.Column(db.String(128))
	time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location = db.Column(db.String(20))
	title = db.Column(db.String(80))
	body = db.Column(db.String(255))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)


