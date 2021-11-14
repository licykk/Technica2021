from flask_login import UserMixin
from datetime import date, datetime
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(unique=True, min_length=1, max_length=40, required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField()
    profile_pic = db.ImageField()
    mood = db.StringField()
    daily_prompt_date = db.StringField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Post(db.Document):
    user = db.ReferenceField('User')
    title = db.StringField(min_length=1, required=True)
    content = db.StringField(min_length=1, required=True)
    date = db.StringField(required=True)

