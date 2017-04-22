import json

import pytest

from online_courses_api.tests.helper import post, get, delete, Joe, is_teachers


def test_create_a_teacher(app):
    resp = post(app, '/teachers', data=Joe)
    assert 'id' in resp
    assert is_teachers(resp, Joe)


def test_get_teacher(app):
    resp = get(app, '/teacher/1')
    assert is_teachers(resp, Joe)


def test_delete_teacher(app):
    resp = delete(app, '/teacher/1')
    assert False  # check db directly


def test_filter_by_first_name(app):
    resp = get(app, '/teachers?first_name=Joe')
    assert resp
    for r in resp:
        assert r['first_name'] == 'Joe'


def test_filter_by_last_name(app):
    resp = get(app, '/teachers?last_name=Moon')
    assert resp
    for r in resp:
        assert r['last_name'] == 'Moon'


def test_filter_by_spec(app):
    resp = get(app, '/teachers?spec=math')
    assert resp
    for r in resp:
        assert 'math' in r['spec']


def test_filter_by_multiply_spec(app):
    resp = get(app, '/teachers?spec=math&spec=physics')
    assert resp
    for r in resp:
        assert 'math' in r['spec']
        assert 'physics' in r['spec']
