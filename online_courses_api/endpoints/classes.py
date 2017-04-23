from flask import request, jsonify
from werkzeug.exceptions import abort

from online_courses_api import app, db
from online_courses_api.endpoints.basic_crud import create_items_endpoint, create_item_endpoint
from online_courses_api.models.klass import Class
from online_courses_api.models.teacher import Teacher

app.route('/classes',
          methods=['GET', 'POST'],
          endpoint='classes_endpoint')(
    create_items_endpoint(Class)
)


app.route('/classes/<int:item_id>',
          methods=['GET', 'PUT', 'DELETE'],
          endpoint='class_endpoint')(
    create_item_endpoint(Class)
)


@app.route('/classes/<int:cid>/teacher/<int:tid>', methods=['PUT', 'DELETE'])
def class_teacher_endpoint(cid, tid):
    c = Class.query.get(cid)
    if not c:
        return abort(404)
    if request.method == 'PUT':
        t = Teacher.query.get(tid)
        if not t:
            return abort(400)
        if c.teacher_id is not None:
            return abort(400)
        if c.spec not in t.specs:
            return abort(400)
        c.teacher_id = t.id
        db.session.commit()
        return jsonify({})
    elif request.method == 'DELETE':
        c.teacher_id = None
        db.session.commit()
        return jsonify({})
