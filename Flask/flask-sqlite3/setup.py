"""
Flask-SQLite3
-------------
This is the description for that library
"""

from setuptools import setup

setup(
    name = 'Flask-SQLite3',
    version = '1.0',
    url = 'http://example.com/flask-sqlite3',
    license = 'MIT',
    author = 'smith adam',
    author_email = 'sogaxili@gmail.com',
    description = 'Very short description',
    long_description = __doc__,
    py_modules = ['flask_sqlite3'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe = False, 
    include_package_data = True,
    playforms = 'any',
    install_requires = ['Flask'],
    classfiers =  [
        'Enviroment :: Web Enviroment',
        'Intended Audience :: Developers', 
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Lanuage :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)