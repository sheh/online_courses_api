import os
import tempfile
import pytest

from online_courses_api.database import init_db
import online_courses_api
from online_courses_api.models.klass import Class
from online_courses_api.models.student import Student
from online_courses_api.models.teacher import Teacher
from online_courses_api.tests.helper import teachers, Joe, students, Kelly, classes
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
def test_data_added(session):
    for t_dict in teachers:
        t = Teacher(**t_dict)
        session.add(t)
    for s_dict in students:
        s = Student(**s_dict)
        session.add(s)
    for c_dict in classes:
        c = Class(**c_dict)
        session.add(c)
    session.commit()


@pytest.fixture(scope='function')
def kelly_in_math_class(session, test_data_added):
    c = Class.query.get('1')
    s = Student.query.get('1')
    s.classes.append(c)
    session.commit()


@pytest.fixture(scope='function')
def kelly_in_english_class(session, test_data_added):
    c = Class.query.get('2')
    s = Student.query.get('1')
    s.classes.append(c)
    session.commit()


@pytest.fixture(scope='function')
def steve_in_english_class(session, test_data_added):
    c = Class.query.get('2')
    s = Student.query.get('2')
    s.classes.append(c)
    session.commit()


@pytest.fixture(scope='function')
def math_class_bind_joe(session, test_data_added):
    c = Class.query.get('1')
    c.teacher_id = 1
    session.commit()


@pytest.fixture(scope='function')
def physics_class_bind_joe(session, test_data_added):
    c = Class.query.get('3')
    c.teacher_id = 1
    session.commit()


@pytest.fixture(scope='function')
def physics_class_bind_mary(session, test_data_added):
    c = Class.query.get('3')
    c.teacher_id = '2'
    session.commit()
