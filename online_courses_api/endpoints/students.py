from flask import request, jsonify
from werkzeug.exceptions import abort

from online_courses_api import app, db
from online_courses_api.endpoints.basic_crud import create_item_endpoint, create_items_endpoint
from online_courses_api.models.klass import Class
from online_courses_api.models.student import Student

app.route('/students',
          methods=['GET', 'POST'],
          endpoint='students_endpoint')(
    create_items_endpoint(Student)
)

app.route('/students/<int:item_id>',
          methods=['GET', 'PUT', 'DELETE'],
          endpoint='student_endpoint')(
    create_item_endpoint(Student)
)


@app.route('/students/<int:sid>/classes/<int:cid>', methods=['PUT', 'DELETE'])
def students_classes_endpoint(sid, cid):
    s = Student.query.get(sid)
    if not s:
        return abort(404)
    if request.method == 'PUT':
        c = Class.query.get(cid)
        if not c:
            return abort(400)
        s.classes.append(c)
        db.session.commit()
        return jsonify({})
    elif request.method == 'DELETE':
        s.classes = list(filter(lambda x: x.id != cid, s.classes))
        db.session.commit()
        return jsonify({})
