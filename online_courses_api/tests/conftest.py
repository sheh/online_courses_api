import os
import tempfile
import pytest

from online_courses_api.database import init_db
import online_courses_api
from online_courses_api.models.student import Student
from online_courses_api.models.teacher import Teacher
from online_courses_api.tests.helper import teachers, Joe, students, Kelly
from sqlalchemy.orm.session import make_transient


@pytest.fixture(scope="session")
def app():
    _app = online_courses_api.app
    db_fd, tmpfile = tempfile.mkstemp()
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + tmpfile
    _app.config['TESTING'] = True
    return _app


@pytest.fixture(scope="session")
def db(app, request):
    _db = online_courses_api.db

    _db.app = app
    _db.create_all()

    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def teachers_added(session):
    for t_dict in teachers:
        t = Teacher(**t_dict)
        session.add(t)
    session.commit()


@pytest.fixture(scope='function')
def students_added(session):
    for s_dict in students:
        s = Student(**s_dict)
        session.add(s)
    session.commit()
