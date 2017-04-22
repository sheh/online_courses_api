import pytest as pytest
import online_courses_api


@pytest.fixture('module')
def app():
    return online_courses_api.app.test_client()


@pytest.fixture('module')
def with_teacher_joe():
    pass