import json


Joe = dict(
    first_name='Joe',
    last_name='Moon',
    spec=['math', 'physics'],
)


Mary = dict(
    first_name='Mary',
    last_name='Smith',
    spec=['english'],
)


Heather = dict(
    first_name='Heather',
    last_name='Moon',
    spec=['physics', 'astronomy'],
)


teachers = (Joe, Mary, Heather)


def is_teachers(resp, *teacher):
    if type(resp) == dict:
        resp = [resp]
    s1 = set(map(
        lambda x: dict(filter(lambda k,v: k != 'id', x.items())),
        resp
    ))
    s2 = set(teachers)
    return s1 == s2


def post(app, url, data):
    resp = app.post(url, data=data)
    assert resp.status_code == 200
    return json.loads(resp.data)


def get(app, url):
    resp = app.get(url)
    assert resp.status_code == 200
    return json.loads(resp.data)


def delete(app, url):
    resp = app.delete(url)
    assert resp.status_code == 200
    return json.loads(resp.data)
