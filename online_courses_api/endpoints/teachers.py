from werkzeug.exceptions import abort

from online_courses_api import app


@app.route('/teachers', methods=['POST', 'GET'])
def teachers_endpoint():
    return abort(500)


@app.route('/teachers/<tid>', methods=['PUT', 'DELETE'])
def teacher_endpoint(tid):
    return abort(500)
