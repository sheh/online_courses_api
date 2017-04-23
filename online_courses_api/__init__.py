import tempfile

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


import online_courses_api.endpoints.teachers
import online_courses_api.endpoints.classes
import online_courses_api.endpoints.students
