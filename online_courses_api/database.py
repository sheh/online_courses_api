from flask import g
from flask_sqlalchemy import SQLAlchemy

from online_courses_api import app, db


def init_db():
    import online_courses_api.models.student_to_class
    import online_courses_api.models.teacher
    import online_courses_api.models.student
    import online_courses_api.models.klass
    db.create_all()
    db.session.commit()
