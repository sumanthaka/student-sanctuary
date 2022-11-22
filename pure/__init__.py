from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

import pymongo

from pure.config import Config

app = Flask(__name__)
app.config.from_object(Config)
client = pymongo.MongoClient(app.config["MONGODB_DATABASE_URI"])
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'student.student_signin'
mail = Mail(app)

from pure.main.routes import main
from pure.super_admin.routes import super_admin
from pure.admin.routes import admin
from pure.faculty.routes import faculty
from pure.student.routes import student
from pure.profile.routes import profile
from pure.announcements.routes import announcement


app.register_blueprint(main)
app.register_blueprint(super_admin)
app.register_blueprint(admin)
app.register_blueprint(faculty)
app.register_blueprint(student)
app.register_blueprint(profile)
app.register_blueprint(announcement)
