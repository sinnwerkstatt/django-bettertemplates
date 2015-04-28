#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-bettertemplates',
    version='0.0.1',
    description='Django Better Templates',
    long_description=readme + '\n\n' + history,
    author='Sinnwerkstatt Medienagentur GmbH',
    author_email='web@sinnwerkstatt.com',
    url='https://github.com/sinnwerkstatt/django-bettertemplates',
    packages=[
        'bettertemplates',
    ],
    package_dir={'bettertemplates': 'bettertemplates'},
    include_package_data=True,
    install_requires=['six'],
    license="BSD",
    zip_safe=False,
    keywords='Django Templates',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
