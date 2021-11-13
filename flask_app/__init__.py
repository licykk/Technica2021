# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
import os
from datetime import datetime

app = Flask(__name__)
app.config["MONGODB_HOST"] = "mongodb://localhost:27017/project_4"
app.config["SECRET_KEY"] = b'\x9e\xdd\xf0\xecU\x85\xa6J`\xe7H\xe8\x8c\x02\xec\xd8'

ALLOWED_EXTENSIONS = {'jpg', 'png'}
# app.config['UPLOAD_FOLDER'] = "/profile_pics"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

from . import routes
