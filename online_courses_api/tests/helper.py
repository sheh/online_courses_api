import json
from collections import namedtuple

from online_courses_api.models import Teacher

Joe = Teacher(
    id=1,
    first_name='Joe',
    last_name='Moon',
    specs=['math', 'physics'],
)


Mary = Teacher(
    id=2,
    first_name='Mary',
    last_name='Smith',
    specs=['physics', 'astronomy'],
)


Heather = Teacher(
    id=3,
    first_name='Heather',
    last_name='Moon',
    specs=['english'],
)


teachers = (Joe, Mary, Heather)


def is_teachers(resp, *teachers):
    if type(resp) == dict:
        resp = [resp]
    s1 = set(map(lambda x: Teacher(**x), resp))
    s2 = set(teachers)
    return s1 == s2


def __request_200(method, *args, **kwargs):
    resp = method(*args, **kwargs)
    assert resp.status_code == 200, f'Response code is {resp.status_code}'
    return json.loads(resp.data)


post = lambda client, url, data: \
    __request_200(client.post, url, data=json.dumps(data), content_type='application/json')
get = lambda client, url: __request_200(client.get, url)
delete = lambda client, url: __request_200(client.delete, url)
put = lambda client, url, data: \
    __request_200(client.put, url, data=json.dumps(data), content_type='application/json')