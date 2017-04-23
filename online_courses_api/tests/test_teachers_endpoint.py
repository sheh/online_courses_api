import json

import pytest
from flask import jsonify

from online_courses_api.models.teacher import Teacher
from online_courses_api.tests.helper import post, get, delete, Joe, put


def test_create_teacher(client, session):
    js = post(client, '/teachers', data=Joe)
    assert js == {**Joe, **dict(id=1)}


def test_create_teacher_with_wrong_data(client, session):
    d = Joe.copy()
    del d['first_name']
    resp = client.post('/teachers', data=json.dumps(d), content_type='application/json')
    assert resp.status_code == 400


def test_get_teacher_not_found(client, session):
    resp = client.get('/teachers/1')
    assert resp.status_code == 404


def test_get_teacher(client, teachers_added):
    js = get(client, '/teachers/1')
    assert js == {**Joe, **dict(id=1)}


def test_delete_teacher(client, teachers_added):
    resp = delete(client, '/teachers/1')
    assert resp == {}


def test_delete_nonexistent_teacher(client, teachers_added):
    resp = delete(client, '/teachers/100500')
    assert resp == {}  # ok, teacher doesnt exist


def test_filter_without_query(client, teachers_added):
    resp = client.get('/teachers')
    assert resp.status_code == 400


def test_filter_wrong_query(client, teachers_added):
    resp = client.get('/teachers?foo=bar')
    assert resp.status_code == 400


def test_filter_by_first_name(client, teachers_added):
    resp = get(client, '/teachers?first_name=Joe')
    assert len(resp) == 1
    for r in resp:
        assert r['first_name'] == 'Joe'


def test_filter_by_last_name(client, teachers_added):
    resp = get(client, '/teachers?last_name=Moon')
    assert len(resp) == 2
    for r in resp:
        assert r['last_name'] == 'Moon'


def test_filter_by_spec(client, teachers_added):
    resp = get(client, '/teachers?spec=math')
    assert len(resp) == 1
    for r in resp:
        assert 'math' in r['specs']


def test_filter_by_multiply_spec(client, teachers_added):
    resp = get(client, '/teachers?spec=math&spec=physics')
    assert resp
    for r in resp:
        assert 'math' in r['specs']
        assert 'physics' in r['specs']


def test_update_teacher_wrong_data(client, teachers_added):
    d = Joe.copy()
    del d['first_name']
    resp = client.put('/teachers/1', data=json.dumps(d), content_type='application/json')
    assert resp.status_code == 400


def test_update_teacher(client, teachers_added):
    d = Joe.copy()
    d['specs'] = Joe['specs'] + ['astronomy']
    resp = put(client, '/teachers/1', data=d)
    assert resp['specs'] == d['specs']


def test_update_nonexistent_teacher(client, teachers_added):
    resp = client.put('/teachers/100500', data=json.dumps(Joe), content_type='application/json')
    assert resp.status_code == 404
