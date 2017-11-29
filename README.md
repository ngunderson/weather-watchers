# Weather Watchers

This is the server portion of a user driven weather network application.

Currently undergoing development.

### INSTALL
The following commands should be run in the currenty directory containing setup.py
It is also recommended to use a local python environment by running:

`python3 -m venv venv3`

and

`source venv3/bin/activate`

To install this package, run:

`pip install .`

If you would like to be able to edit the installed package, run:

`pip install -e .`

#### Helpful Notes

If needed run,

`pip install setuptools --upgrade`

if a "bdist" error occurs


To execute the tests, run:

`python setup.py test`

or

`python weather_server/test_server.py`
