from flask import jsonify
from flask import request
from werkzeug.exceptions import abort

from online_courses_api import app
from online_courses_api.db_layer import get_teacher, create_teacher, del_teacher, filter_teachers, update_teacher
from online_courses_api.models import Teacher


def create_item(model, request):
    item = model(**request.get_json())
    item.store()
    return item


def get_items(model, filter):
    items = model.filter(**request.args)
    return items


def all_items(model):
    if request.method == 'POST':
        item = model.from_json(**request.get_json())
        if not item:
            return abort(400)
        store_item = item.save()
        if not store_item:
            return abort(400)
        return store_item
    elif request.method == 'GET':
        return get_items(model, filter)


@app.route('/teachers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def one_item(model, id):
    if request.method == 'GET':
        model(id)
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

