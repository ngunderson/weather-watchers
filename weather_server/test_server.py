from weather_server.server import create_app
from weather_server.db.model import db
from flask_testing import TestCase

import unittest
import warnings

# self.client will access the initialized app

class WeatherServerBase(TestCase):

    cfg = {
        "SQLALCHEMY_DATABASE_URI" : "sqlite:///test.db",
        "TESTING" : True
    }

    def create_app(self):
        return create_app(self.cfg)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestAPIViews(WeatherServerBase):

    def test_empty_device_request(self):
        response = self.client.get("/devices")
        self.assertEqual([], response.json)

    #def test_post_device(self):


class TestFrontEndViews(WeatherServerBase):

    def test_home_template_used(self):
        response = self.client.get("/")
        self.assert_template_used("index.html")

    def test_mainjs_used(self):
        warnings.simplefilter("ignore", ResourceWarning)

        response = self.client.get("/static/main.js")

        jsfile = open("static/main.js", "r")
        jscontent = jsfile.read()
        jsfile.close()

        self.assertEqual(jscontent, response.data.decode('utf-8'))

    def test_jqueryjs_used(self):
        warnings.simplefilter("ignore", ResourceWarning)

        response = self.client.get("/static/jquery-3.2.1.min.js")

        jsfile = open("static/jquery-3.2.1.min.js", "r")
        jscontent = jsfile.read()
        jsfile.close()

        self.assertEqual(jscontent, response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
