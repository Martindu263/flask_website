from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
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

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('密码重置')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('密码重置')

class EditProfileForm(FlaskForm):
    username = StringField('修改用户名', validators=[DataRequired()])
    about_me = TextAreaField('更新我的介绍', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')

    #验证用户名，如果在表单中输入的用户名与原始用户名相同，那么就没必要检查数据库是否有重复了。
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('用户名被占用，更新请换个名字')

class PostForm(FlaskForm):
    post = TextAreaField('发表你的信息吧', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('发送')