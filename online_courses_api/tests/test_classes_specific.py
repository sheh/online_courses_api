from operator import itemgetter

from online_courses_api.models.klass import Class
from online_courses_api.tests.helper import put, delete, get


def test_bind_to_teacher(client, test_data_added):
    resp = put(client, f'/classes/1/teacher/1', data={})
    assert resp == {}
    assert Class.query.get(1).teacher_id == 1


def test_bind_to_nonexistent_teacher_fails(client, test_data_added):
    resp = client.put('/classes/1/teacher/100500')
    assert resp.status_code == 400


def test_bind_already_bind_fails(client, physics_class_bind_joe):
    resp = client.put('/classes/3/teacher/2')
    assert resp.status_code == 400


def test_bind_not_matching_spec(client, test_data_added):
    resp = client.put('/classes/1/teacher/2')
    assert resp.status_code == 400


def test_unbind(client, math_class_bind_joe):
    resp = delete(client, '/classes/1/teacher/1')
    assert resp == {}


def test_unbind_not_bind(client, test_data_added):
    resp = delete(client, '/classes/1/teacher/1')
    assert resp == {}


def test_filter_by_teacher(client, math_class_bind_joe, physics_class_bind_joe):
    resp = get(client, '/classes?teacher=1')
    assert len(resp) == 2
    assert set(map(itemgetter('name'), resp)) == {'math1', 'phy1'}


def test_filter_by_several_teacher(client, math_class_bind_joe, physics_class_bind_mary):
    resp = get(client, '/classes?teacher=1&teacher=2&teacher=3')
    assert len(resp) == 2
    assert set(map(itemgetter('name'), resp)) == {'math1', 'phy1'}
