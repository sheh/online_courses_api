from flask import jsonify
from flask import request
from werkzeug.exceptions import abort

from online_courses_api import app, db
from online_courses_api.models.teacher import Teacher


def create_items_endpoint(model):
    def ep():
        if request.method == 'POST':
            try:
                t = model(**request.get_json())
            except TypeError:
                return abort(400)
            db.session.add(t)
            db.session.commit()
            return jsonify(t.as_dict())
        elif request.method == 'GET':
            ts = model.filter(**request.args)
            if ts is None:
                return abort(400)
            return jsonify([t.as_dict() for t in ts])
    return ep


def create_item_endpoint(model):
    def ep(item_id):
        item = model.query.get(item_id)
        if request.method == 'GET':
            return jsonify(item.as_dict()) if item else abort(404)
        elif request.method == 'DELETE':
            if item:
                db.session.delete(item)
                db.session.commit()
            return jsonify({})  # return just empty response here
        elif request.method == 'PUT':
            if not item:
                return abort(404)
            t_req_json = request.get_json()
            try:
                t = model(id=item_id, **t_req_json)
            except TypeError:
                return abort(400)
            else:
                db.session.merge(t)
                db.session.commit()
            t = model.query.get(item_id)
            return jsonify(t.as_dict())
    return ep

