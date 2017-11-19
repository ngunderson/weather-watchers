from setuptools import setup, find_packages

setup(
    name='weather-app',
    version='1.0',
    packages=find_packages(),
    install_requires=['flask', 'flask-sqlalchemy', 'flask-marshmallow', 'marshmallow-sqlalchemy', 'python-dateutil']
)
