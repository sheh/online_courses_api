import json

import pytest

from online_courses_api.tests.helper import post, get, delete, Joe, put, Kelly, MathClass


@pytest.mark.parametrize("endpoint,item", [
    ("/teachers", Joe),
    ("/students", Kelly),
    ("/classes", MathClass),
])
def test_create_item(client, session, endpoint, item):
    resp = post(client, endpoint, data=item)
    assert resp == {**item, **dict(id=1)}


@pytest.mark.parametrize("endpoint,item", [
    ("/teachers", Joe),
    ("/students", Kelly),
    ("/classes", MathClass),
])
def test_create_item_with_partial_data_fails(client, session, endpoint, item):
    d = item.copy()
    d.popitem()
    resp = client.post(endpoint, data=json.dumps(d), content_type='application/json')
    assert resp.status_code == 400


@pytest.mark.parametrize("endpoint,item", [
    ("/teachers", Joe),
    ("/students", Kelly),
    ("/classes", MathClass),
])
def test_create_item_with_extra_data_fails(client, session, endpoint, item):
    d = item.copy()
    d.update(foo='bar')
    resp = client.post(endpoint, data=json.dumps(d), content_type='application/json')
    assert resp.status_code == 400


@pytest.mark.parametrize("endpoint", [
    "/teachers",
    "/students",
    "/classes",
])
def test_get_item_nonexistent_item_fails(client, session, endpoint):
    resp = client.get(f'{endpoint}/1')
    assert resp.status_code == 404


@pytest.mark.parametrize("endpoint,item", [
    ("/teachers", Joe),
    ("/students", Kelly),
    ("/classes", MathClass),
])
def test_get_item(client, test_data_added, endpoint, item):
    js = get(client, f'{endpoint}/1')
    assert js == {**item, **dict(id=1)}


@pytest.mark.parametrize("endpoint", [
    "/teachers",
    "/students",
    "/classes",
])
def test_delete_item(client, test_data_added, endpoint):
    resp = delete(client, f'{endpoint}/1')
    assert resp == {}


@pytest.mark.parametrize("endpoint", [
    "/teachers",
    "/students",
    "/classes",
])
def test_delete_nonexistent_item(client, session, endpoint):
    resp = delete(client, f'{endpoint}/1')
    assert resp == {}  # ok, teacher does not exist


@pytest.mark.parametrize("endpoint", [
    "/teachers",
    "/students",
    "/classes",
])
def test_filter_item_without_query_fails(client, test_data_added, endpoint):
    resp = client.get(endpoint)
    assert resp.status_code == 400


@pytest.mark.parametrize("endpoint", [
    "/teachers",
    "/students",
    "/classes",
])
def test_filter_item_wrong_query_fails(client, test_data_added, endpoint):
    resp = client.get(f'{endpoint}?foo=bar')
    assert resp.status_code == 400


@pytest.mark.parametrize("endpoint,first_name,found", [
    ("/teachers", 'Joe', 1),
    ("/students", 'Kelly', 1),
])
def test_filter_item_by_first_name(client, test_data_added, endpoint, first_name, found):
    resp = get(client, f'{endpoint}?first_name={first_name}')
    assert len(resp) == found
    for r in resp:
        assert r['first_name'] == first_name


@pytest.mark.parametrize("endpoint,last_name,found", [
    ("/teachers", 'Moon', 2),
    ("/students", 'Williams', 1),
])
def test_filter_item_by_last_name(client, test_data_added, endpoint, last_name, found):
    resp = get(client, f'{endpoint}?last_name={last_name}')
    assert len(resp) == found
    for r in resp:
        assert r['last_name'] == last_name


def test_filter_item_by_spec(client, test_data_added):
    resp = get(client, '/teachers?spec=math')
    assert len(resp) == 1
    for r in resp:
        assert 'math' in r['specs']


def test_filter_item_by_multiply_spec(client, test_data_added):
    resp = get(client, '/teachers?spec=math&spec=physics')
    assert resp
    for r in resp:
        assert 'math' in r['specs']
        assert 'physics' in r['specs']


@pytest.mark.parametrize("endpoint,item", [
    ("/teachers", Joe),
    ("/students", Kelly),
    ("/classes", MathClass),
])
def test_update_item_wrong_data(client, test_data_added, endpoint, item):
    d = item.copy()
    d.popitem()
    resp = client.put(f'{endpoint}/1', data=json.dumps(d), content_type='application/json')
    assert resp.status_code == 400


@pytest.mark.parametrize("endpoint,item,field", [
    ("/teachers", Joe, 'first_name'),
    ("/students", Kelly, 'last_name'),
    ("/classes", MathClass, 'name'),
])
def test_update_item(client, test_data_added, endpoint, item, field):
    d = item.copy()
    d[field] = 'foo'
    resp = put(client, f'{endpoint}/1', data=d)
    assert resp[field] == 'foo'


def test_update_item_specs(client, test_data_added):
    d = Joe.copy()
    d['specs'] = Joe['specs'] + ['astronomy']
    resp = put(client, '/teachers/1', data=d)
    assert resp['specs'] == d['specs']


@pytest.mark.parametrize("endpoint", [
    "/teachers",
    "/students",
    "/classes",
])
def test_update_item_nonexistent(client, session, endpoint):
    resp = client.put(f'{endpoint}/1', data=json.dumps(Joe), content_type='application/json')
    assert resp.status_code == 404
