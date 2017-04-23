from sqlalchemy import Column, Integer, String

from online_courses_api import db


class Teacher(db.Model):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), unique=False)
    last_name = Column(String(30), unique=False)
    specs = Column(String(30), unique=False)

    __filter_keys = {'first_name', 'last_name', 'spec'}

    def __init__(self, first_name, last_name, specs, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.specs = ','.join(specs)
        self.id = id

    def as_dict(self):
        d = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'specs': self.specs.split(',')
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
        if param == 'spec':
            return cls.query.filter(Teacher.specs.like(f'%{val[0]}%')).all()
        else:
            return cls.query.filter_by(**{param: val[0]}).all()
