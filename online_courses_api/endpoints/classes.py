from werkzeug.exceptions import abort

from online_courses_api import app


@app.route('/classes', methods=['POST', 'GET'])
def classes_endpoint():
    return abort(500)


@app.route('/classes/<cid>', methods=['PUT', 'DELETE'])
def class_endpoint(cid):
    return abort(500)


@app.route('/classes/<cid>/teacher/<tid>', methods=['PUT', 'DELETE'])
def class_teacher_endpoint(cid, tid):
    return abort(500)
