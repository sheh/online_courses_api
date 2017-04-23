from flask import jsonify
from flask import request
from werkzeug.exceptions import abort

from online_courses_api import app, db
from online_courses_api.models.teacher import Teacher


@app.route('/teachers', methods=['GET', 'POST'])
def teachers_endpoint():
    if request.method == 'POST':
        try:
            t = Teacher(**request.get_json())
        except TypeError:
            return abort(400)
        db.session.add(t)
        db.session.commit()
        return jsonify(t.as_dict())
    elif request.method == 'GET':
        ts = Teacher.filter(**request.args)
        if ts is None:
            return abort(400)
        return jsonify([t.as_dict() for t in ts])


@app.route('/teachers/<int:tid>', methods=['GET', 'PUT', 'DELETE'])
def teacher_endpoint(tid):
    t = Teacher.query.get(tid)
    if request.method == 'GET':
        if not t:
            return abort(404)
        return jsonify(t.as_dict())
    elif request.method == 'DELETE':
        if t:
            db.session.delete(t)
            db.session.commit()
        return jsonify({})  # return just empty response here
    elif request.method == 'PUT':
        if not t:
            return abort(404)
        t_req_json = request.get_json()
        t_req_json.update(id=tid)
        t_req_json.pop('id', None)  # ignore id from request
        try:
            t = Teacher(**t_req_json)
        except TypeError as ex:
            return abort(400)
        db.session.commit()
        return jsonify(t.as_dict())

