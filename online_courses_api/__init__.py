from flask import Flask

app = Flask(__name__)

import online_courses_api.endpoints.teachers
import online_courses_api.endpoints.classes
import online_courses_api.endpoints.students