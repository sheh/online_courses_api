from online_courses_api.models import Student
from online_courses_api.tests.helper import post, Kelly


def test_create_student(client, db, kelly):
    del kelly['id']
    resp = post(client, '/students', data=kelly)
    assert Student(**resp) == Kelly


def test_create_student_with_wrong_data_400(client, db, kelly):
    del kelly['id']
    del kelly['first_name']
    resp = client.post('/students', data=kelly)
    assert resp.status_code == 400
