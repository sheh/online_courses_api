from operator import itemgetter

from online_courses_api.models.student import Student
from online_courses_api.tests.helper import post, Kelly, put, delete, get


def test_add_class(client, test_data_added):
    resp = put(client, '/students/1/classes/1', data={})
    assert resp == {}
    assert len(Student.query.get('1').classes) == 1
    assert Student.query.get('1').classes[0].id == 1


def test_add_class_if_class_doesnt_exist_fails(client, test_data_added):
    resp = client.put('/students/1/classes/100500')
    assert resp.status_code == 400


def test_delete_from_class(client, kelly_in_math_class):
    resp = delete(client, '/students/1/classes/1')
    assert resp == {}
    assert not any([c.id == 1 for c in Student.query.get('1').classes])


def test_delete_from_class_if_not_added_before(client, test_data_added):
    resp = delete(client, '/students/1/classes/100500')
    assert resp == {}


def test_filter_by_class(client, kelly_in_math_class, kelly_in_english_class):
    resp = get(client, '/students?class=1')
    assert len(resp) == 1
    assert resp[0]['first_name'] == 'Kelly'


def test_filter_by_several_classes(client, kelly_in_math_class, kelly_in_english_class, steve_in_english_class):
    resp = get(client, '/students?class=1&class=2')
    assert len(resp) == 2
    assert set(map(itemgetter('first_name'), resp)) == {'Kelly', 'Steve'}
