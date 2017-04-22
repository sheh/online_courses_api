from flask import jsonify
from flask import request
from werkzeug.exceptions import abort

from online_courses_api import app
from online_courses_api.db_layer import get_teacher, create_teacher, del_teacher, filter_teachers, update_teacher
from online_courses_api.models import Teacher


@app.route('/teachers', methods=['GET', 'POST'])
def teachers_endpoint():
    if request.method == 'POST':
        try:
            t = Teacher(id=None, **request.get_json())
        except TypeError:
            return abort(400)
        inserted_t = create_teacher(t)
        if not inserted_t:
            return abort(400)
        return jsonify(inserted_t._asdict())
    elif request.method == 'GET':
        for f in ('first_name', 'last_name', 'spec'):
            if request.args.get(f):
                ts = filter_teachers(f, request.args[f])
                return jsonify(list(map(lambda x: x._asdict(), ts)))
        return abort(400)


@app.route('/teachers/<int:tid>', methods=['GET', 'PUT', 'DELETE'])
def teacher_endpoint(tid):
    if request.method == 'GET':
        t = get_teacher(tid)
        if not t:
            return abort(404)
        return jsonify(t._asdict())
    elif request.method == 'DELETE':
        del_teacher(tid)
        return jsonify({})  # return just empty response here
    elif request.method == 'PUT':
        t_req_json = request.get_json()
        t_req_json.pop('id', None)  # ignore id from request
        try:
            t_req = Teacher(id=tid, **t_req_json)
        except TypeError:
            return abort(400)
        t_resp = update_teacher(tid, t_req)
        return jsonify(t_resp._asdict()) if t_resp is not None else abort(400)

