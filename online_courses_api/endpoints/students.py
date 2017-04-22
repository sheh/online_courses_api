from werkzeug.exceptions import abort

from online_courses_api import app


@app.route('/students', methods=['POST', 'GET'])
def students_endpoint():
    return abort(500)


@app.route('/students/<sid>', methods=['PUT', 'DELETE'])
def student_endpoint(sid):
    return abort(500)


@app.route('/students/<sid>/classes/<cid>', methods=['PUT', 'DELETE'])
def student_class_endpoint(sid, cid):
    return abort(500)
