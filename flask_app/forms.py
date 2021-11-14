from wtforms.fields.core import RadioField, SelectMultipleField
from wtforms.widgets.core import Input
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, SelectMultipleField, SelectField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from .models import User


class PostForm(FlaskForm):

    title = StringField(
        "Title", validators=[InputRequired(), Length(min=0, max=60)]
    )
    ##blog 
    content = TextAreaField(
        "What's on your mind?", validators=[InputRequired(), Length(min=0, max=200)]
    )
    tags = SelectMultipleField("Tags", choices=[("Sad","Sad"), ("Happy","Happy"), ("Afraid","Afraid"), ("Angry","Angry"), ("Surprised","Surprised"), ("Disgusted","Disgusted"), ("Neutral","Neutral")])
    submit = SubmitField("Post")
 
# HOME

class MoodForm(FlaskForm):
    mood = RadioField("Mood", choices=["Sad", "Happy", "Afraid", "Angry", "Surprised", "Disgusted", "Neutral"])
    submit = SubmitField("Check in")

class PromptForm(FlaskForm):
    content = TextAreaField("Prompt", validators=[InputRequired(), Length(min=1)])
    submit = SubmitField("Write")

# USER MANAGEMENT

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")