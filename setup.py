"""
Flask-GoogleCharts
==================

Adds Google Charts API support to Flask.

Links
=====

* `Source Code <https://github.com/wikkiewikkie/flask-googlecharts>`_
* `Issues <https://github.com/wikkiewikkie/flask-googlecharts/issues>`_

"""
from setuptools import setup

extra = {}
install_requires = ['Flask>=0.10.1']
setup(
    name='Flask-GoogleCharts',
    version='0.0.2',
    url='http://github.com/wikkiewikkie/flask-googlecharts/',
    license='MIT',
    author='Kevin Schellenberg',
    author_email='wikkiewikkie@gmail.com',
    description='Google Charts API support for Flask',
    long_description=__doc__,
    packages=['flask_googlecharts'],
    package_data={
        'flask_googlecharts': ['templates/*', 'static/*'], },
    py_modules=['flask_googlecharts'],
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    test_suite='test_googlecharts',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    **extra)
