import os
import tempfile
import pytest
from copy import deepcopy

from online_courses_api.db_layer import init_db, get_db
import online_courses_api
from online_courses_api.tests.helper import teachers, Joe
import pytest_flask


@pytest.fixture("module")
def app():
    return online_courses_api.app


@pytest.fixture("function")
def db(app):
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    init_db()
    yield get_db()
    os.close(db_fd)
    os.unlink(online_courses_api.app.config['DATABASE'])


@pytest.fixture('function')
def teachers_added(db):
    db.executemany(
        'INSERT INTO teachers(rowid, first_name, last_name, specs) VALUES (?, ?, ?, ?)',
        [(t.id, t.first_name, t.last_name, ','.join(t.specs)) for t in teachers],
    )
    return db.commit()


@pytest.fixture('function')
def joe():
    return deepcopy(Joe._asdict())
