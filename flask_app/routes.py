import bson
from flask import render_template, request, redirect, url_for, flash
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from mongoengine.base.fields import ObjectIdField
from werkzeug.utils import secure_filename
from . import app, bcrypt
from datetime import datetime

from .models import (
    User, 
    Post,
    load_user
)
from .forms import (
    LoginForm,
    MoodForm,
    PostForm,
    PromptForm,
    RegistrationForm,
)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/posts/<post_id>")
@login_required
def post_detail(post_id):
    post=Post.objects(id=post_id).first()
    return render_template("post_detail.html", post=post)

@app.route("/user/<user_id>")
@login_required
def user_detail(user_id):
    user=User.objects(id=user_id).first()
    posts=Post.objects(user=user)
    return render_template("user_detail.html", user=user, posts=posts, user_mood=current_user.mood)

# USER MANAGEMENT PAGES - LOGIN, REGISTER, ETC.

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=bcrypt.generate_password_hash(form.password.data))
        user.save()
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if (user is not None and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)
            return redirect(url_for('index', username=user.username))
        else:
            flash("Invalid username or password")
    
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# UNIQUE USER PAGES
@app.route("/feed")
@login_required
def feed():
    posts = reversed(Post.objects())
    return render_template("feed.html", posts=posts)

@app.route("/account", methods=["GET", "POST"])
@login_required
def profile():
    posts = Post.objects(user=current_user)

    mood = MoodForm()
    if mood.validate_on_submit():
        current_user.modify(mood=mood.mood.data)
        return redirect(url_for("profile"))

    return render_template("account.html", posts=posts, mood_form=mood, current_mood=current_user.mood)

@app.route("/homepage", methods=["GET", "POST"])
@login_required
def homepage():
    prompt = "What do I know to be true that I didn’t know a year ago?"

    prompt_form = PromptForm()
    if prompt_form.validate_on_submit():
        post = Post(
            title="Prompt:" + prompt,
            user=current_user._get_current_object(),
            content=prompt_form.content.data,
            date=datetime.now().strftime("%B %d, %Y at %H:%M:%S"),
        )

        current_user.modify(daily_prompt_date=datetime.now().strftime("%B %d %Y"))
        
        post.save()

        return redirect(url_for("homepage"))

    return render_template("homepage.html", prompt=prompt, prompt_form=prompt_form, date=datetime.now().strftime("%B %d %Y"))

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    form = PostForm()

    print(form.tags)
    if form.validate_on_submit():
        post = Post(
            user=current_user._get_current_object(),
            title=form.title.data,
            content=form.content.data,
            tags=form.tags.data,
            date=datetime.now().strftime("%B %d, %Y at %H:%M:%S"),
        )

        post.save()

        return redirect(url_for("post_detail", post_id=post.id))

    return render_template("post.html", form=form)