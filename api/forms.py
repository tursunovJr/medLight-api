from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required


class LoginForm(Form):
    username = StringField("username", validators=[Required()])
    password = PasswordField("password", validators=[Required()])
    remember_me = BooleanField("remember_me", default=False)
    submit = SubmitField()