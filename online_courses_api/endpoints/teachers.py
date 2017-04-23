from flask import jsonify
from flask import request
from werkzeug.exceptions import abort

from online_courses_api import app, db
from online_courses_api.endpoints.basic_crud import create_items_endpoint, create_item_endpoint
from online_courses_api.models.klass import Class
from online_courses_api.models.student import Student
from online_courses_api.models.teacher import Teacher


app.route('/teachers',
          methods=['GET', 'POST'],
          endpoint='teachers_endpoint')(
    create_items_endpoint(Teacher)
)


app.route('/teachers/<int:item_id>',
          methods=['GET', 'PUT', 'DELETE'],
          endpoint='teacher_endpoint')(
    create_item_endpoint(Teacher)
)

