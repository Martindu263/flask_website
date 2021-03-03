from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

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