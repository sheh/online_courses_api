from sqlalchemy import Column, Integer, String

from online_courses_api import db
from online_courses_api.models.teacher import Teacher


class Class(db.Model):
    __tablename__ = 'class'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=False)
    description = Column(String(100), unique=False)
    spec = Column(String(30), unique=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    __filter_keys = {'name', 'description', 'spec', 'teacher'}

    def __init__(self, name, description, spec, id=None):
        self.name = name
        self.description = description
        self.spec = spec
        self.id = id

    def as_dict(self):
        d = {
            'name': self.name,
            'description': self.description,
            'spec': self.spec,
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
        if param == 'description':
            return cls.query.filter(Class.specs.like(f'%{val[0]}%')).all()
        elif param == 'teacher':
            return cls.query.filter(Class.teacher_id.in_(val)).all()
        else:
            return cls.query.filter_by(**{param: val[0]}).all()
