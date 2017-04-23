from flask import g
from flask_sqlalchemy import SQLAlchemy

from online_courses_api import app, db


def init_db():
    import online_courses_api.models.teacher
    db.create_all()
