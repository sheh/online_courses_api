from sqlalchemy import Column, Integer, String
from online_courses_api.database import Base


class Klass(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=False)
    description = Column(String(100), unique=False)
    spec = Column(String(30), unique=False)

    def __init__(self, name, description, spec):
        self.first_name = name
        self.last_name = description
        self.specs = spec
