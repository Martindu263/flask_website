from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired()])
	password = PasswordField('密码', validators=[DataRequired()])
	remember_me = BooleanField('记住本次登陆')
	submit = SubmitField('登陆')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '再次输入密码', validators=[DataRequired(), EqualTo('password')])
    phone_number = StringField('手机号码', validators=[DataRequired()])
    isteacher = BooleanField('是否是老师')
    submit = SubmitField('提交注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('请更换一个用户名。')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱重复了，请更换邮箱。')

    def validate_phone_number(self, phone_number):
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if user is not None:
            raise ValidationError('电话重复了，请更换电话注册。')