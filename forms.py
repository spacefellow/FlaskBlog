from wtforms import StringField, PasswordField
from models import User
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email, Regexp, Optional, ValidationError


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(min=3, max=72)])
    username = StringField(validators=[Optional()])


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp("^[A-Za-z]*$", 0, "Usernames must have only letters, numbers, dots or underscores", ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_uname(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")
