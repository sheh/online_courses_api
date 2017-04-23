from flask_sqlalchemy import Model
from sqlalchemy import Column, Integer, String


class Student(Model):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), unique=False)
    last_name = Column(String(30), unique=False)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
