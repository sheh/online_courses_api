import tempfile

from flask import Flask

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'


import online_courses_api.endpoints.teachers
import online_courses_api.endpoints.classes
import online_courses_api.endpoints.students
