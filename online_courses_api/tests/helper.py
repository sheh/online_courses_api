import json

from online_courses_api.models.teacher import Teacher
from online_courses_api.models.student import Student

Joe = dict(
    first_name='Joe',
    last_name='Moon',
    specs=['math', 'physics'],
)


Mary = dict(
    first_name='Mary',
    last_name='Smith',
    specs=['physics', 'astronomy'],
)


Heather = dict(
    first_name='Heather',
    last_name='Moon',
    specs=['english'],
)


teachers = (Joe, Mary, Heather)


Kelly = dict(
    first_name='Kelly',
    last_name='Williams',
)


Steve = dict(
    first_name='Steve',
    last_name='Young',
)

students = (Kelly, Steve)


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