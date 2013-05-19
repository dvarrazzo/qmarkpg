#!/usr/bin/env python
"""
qmarkpg -- setup script
"""

classifiers = """
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Database
Topic :: Database :: Front-Ends
Topic :: Software Development
Topic :: Software Development :: Libraries :: Python Modules
"""


import os
from setuptools import setup

# Grab the version without importing the module
# or we will get import errors on install if prerequisites are still missing
fn = os.path.join(os.path.dirname(__file__), 'qmarkpg.py')
f = open(fn)
try:
    for line in f:
        if line.startswith('__version__ ='):
            version = line.split("'")[1]
            break
    else:
        raise ValueError('cannot find __version__ in the qmarkpg module')
finally:
    f.close()

try:
    readme = open('README.rst').read()
except Exception:
    description = long_description = None
else:
    description = readme.splitlines()[0]
    long_description = '\n'.join(readme.splitlines()[3:])


setup(
    name = 'qmarkpg',
    author = 'Daniele Varrazzo',
    author_email = 'daniele.varrazzo@gmail.com',
    url = 'https://github.com/dvarrazzo/qmarkpg',
    license = 'LGPL',
    py_modules = ['qmarkpg'],
    test_suite = 'tests',
    description = description,
    long_description = long_description,
    classifiers = [x for x in classifiers.split('\n') if x],
    zip_safe = False,   # because fuck off
    version = version,
    use_2to3 = True, )
