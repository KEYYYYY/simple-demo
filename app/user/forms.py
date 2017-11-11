from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

from app import avatars


class UserForm(FlaskForm):
    username = StringField(label='用户名', validators=[
        DataRequired(message='必须输入用户名'),
    ])
    avatar = FileField(label='更换头像', validators=[
        FileAllowed(avatars, message='请选择图片上传'),
    ])
    submit = SubmitField(label='更新')
