#!/usr/bin/env python

from distutils.core import setup

import sys

if sys.version_info < (3, 6):
    sys.exit('Python < 3.6 is not supported')


setup(name='online_courses_api',
      version='1.0',
      description='Online courses REST API',
      author_email='shehbox@gmail.com',
      url='https://github.com/sheh/online_courses_api',
      dependencies=[
          'Flask', 'Flask-SQLAlchemy', 'Flask-Script'
      ],
      packages=['online_courses_api'],
)