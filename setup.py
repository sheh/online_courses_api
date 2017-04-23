#!/usr/bin/env python3

from distutils.core import setup

import sys

from setuptools import find_packages

if sys.version_info < (3, 6):
    sys.exit('Python < 3.6 is not supported, (used {})'.format(sys.version_info))


setup(name='online_courses_api',
      version='1.0',
      description='Online courses REST API',
      author_email='shehbox@gmail.com',
      url='https://github.com/sheh/online_courses_api',
      install_requires=[
          'Flask', 'Flask-SQLAlchemy', 'Flask-Script'
      ],
      packages=find_packages(),
      tests_require=[
            'pytest'
      ],
      scripts=['run_app.py'],
)