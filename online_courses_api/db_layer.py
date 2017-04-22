import sqlite3

from online_courses_api import app
from flask import g

from online_courses_api.models import Teacher


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def get_teacher(tid):
    db = get_db()
    c = db.execute('SELECT * FROM teachers WHERE rowid=?', [tid])
    record = c.fetchone()
    if not record:
        return None
    return __teacher_from_db(record)


def filter_teachers(param, val):
    db = get_db()
    if param == 'spec':
        c = db.execute("SELECT * FROM teachers WHERE specs LIKE ?", ('%' + val + '%',))
    else:
        # TODO param is checked above, but anyway we must use safe substitution
        c = db.execute(f"SELECT * FROM teachers WHERE {param}=?", (val, ))
    ts = map(__teacher_from_db, c.fetchall())
    if param == 'spec':  # filter by exact matching
        ts = filter(lambda t: val in t.specs, ts)
    return ts


def del_teacher(tid):
    db = get_db()
    db.execute('DELETE FROM teachers WHERE rowid=?', [tid])
    db.commit()


def create_teacher(teacher):
    db = get_db()
    c = db.execute(
        'INSERT INTO teachers VALUES (?, ?, ?, ?)',
        __teacher_to_db(teacher),
    )
    db.commit()
    # TODO this is not thread safe!
    # TODO check data the same
    db_teacher = get_teacher(c.lastrowid)
    return db_teacher


def update_teacher(tid, teacher):
    db = get_db()
    c = db.execute(
        'UPDATE teachers SET first_name=?, last_name=?, specs=? WHERE id=?',
        list(__teacher_to_db(teacher))[1:] + [tid],
    )
    db.commit()
    if c.rowcount == 1:
        return get_teacher(tid)
    else:
        return None


def __teacher_to_db(t):
    return t.id, t.first_name, t.last_name, ','.join(t.specs)


def __teacher_from_db(record):
    return Teacher(record[0], record[1], record[2], record[3].split(','))