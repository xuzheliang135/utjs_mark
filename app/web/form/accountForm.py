from wtforms import Form, PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from model.user import User


class LoginForm(Form):
    username = StringField('用户名', validators=[DataRequired(message='用户名不可以为空'), Length(1, 20)])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可以为空，请输入你的密码')])


class SignUpForm(LoginForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 10)])
    team_id = IntegerField('组别', validators=[DataRequired(), NumberRange(1, 3)])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('已被注册')


class VoteForm(Form):
    lecturer = StringField("演讲者")
    content = IntegerField('内容分数', validators=[NumberRange(0, 10, message="分数超限")])
    gesture = IntegerField('肢体分数', validators=[NumberRange(0, 40, message="分数超限")])
    voice = IntegerField('声音分数', validators=[NumberRange(0, 50, message="分数超限")])
