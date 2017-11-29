from setuptools import setup, find_packages
import os

setup(
    name='weather_server',
    version='1.0',
    packages=find_packages(),
    package_data={
        'weather_server': [os.path.join('templates', 'index.html'),
                           os.path.join('static', 'main.js'),
                           os.path.join('static', 'jquery-3.2.1.min.js')]
    },
    include_package_data=True,
    install_requires=['flask', 'flask-sqlalchemy', 'flask-marshmallow', 'marshmallow-sqlalchemy', 'python-dateutil', 'wheel'],
    extras_require={
        'test': ['flask-testing', 'blinker']
    }
)
