from sqlalchemy import Column, Integer, String

from online_courses_api import db
from online_courses_api.models.klass import Class
from online_courses_api.models.student_to_class import student_to_class_table


class Student(db.Model):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), unique=False)
    last_name = Column(String(30), unique=False)

    classes = db.relationship('Class', secondary=student_to_class_table,
                              backref=db.backref('students'))

    __filter_keys = {'first_name', 'last_name', 'class'}

    def __init__(self, first_name, last_name, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id

    def as_dict(self):
        d = {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        if self.id:
            d.update(id=self.id)
        return d

    @classmethod
    def filter(cls, **kwargs):
        if len(kwargs) != 1:
            return None
        param, val = kwargs.popitem()
        if param not in cls.__filter_keys or not val:
            return None
        if param == 'class':
            return cls.query.filter(Student.classes.any(Class.id.in_(val)))
        else:
            return cls.query.filter_by(**{param: val[0]}).all()
