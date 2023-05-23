from flask_socketio import SocketIO

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

import pymongo
import mysql.connector
from sqlalchemy import create_engine

# from pure.config import Config
from pure.configlocal import Config


app = Flask(__name__)
app.config.from_object(Config)
client = pymongo.MongoClient(app.config["MONGODB_DATABASE_URI"])
sql_client = mysql.connector.connect(host=app.config["MYSQL_DATABASE_HOST"],
                                     port=app.config["MYSQL_DATABASE_PORT"],
                                     user=app.config["MYSQL_DATABASE_USER"],
                                     database="student_sanctuary")
engine = create_engine(app.config["MYSQL_DATABASE_URI"])
cursor = sql_client.cursor()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'student.student_signin'
mail = Mail(app)
socketio = SocketIO(app)

from pure.main.routes import main
from pure.super_admin.routes import super_admin
from pure.admin.routes import admin
from pure.faculty.routes import faculty
from pure.student.routes import student
from pure.profile.routes import profile
from pure.announcements.routes import announcement
from pure.chat.routes import chat
from pure.study_material.routes import study_material
from pure.feedback.routes import feedback
from pure.ads.routes import ads
from pure.errors.routes import page_not_found, page_forbidden

app.register_blueprint(main)
app.register_blueprint(super_admin)
app.register_blueprint(admin)
app.register_blueprint(faculty)
app.register_blueprint(student)
app.register_blueprint(profile)
app.register_blueprint(announcement)
app.register_blueprint(chat)
app.register_blueprint(study_material)
app.register_blueprint(feedback)
app.register_blueprint(ads)
app.register_error_handler(404, page_not_found)
app.register_error_handler(403, page_forbidden)
