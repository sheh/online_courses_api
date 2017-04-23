from online_courses_api import db

student_to_class_table = db.Table('student_to_class',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)
