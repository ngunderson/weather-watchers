from weather_server.server import create_app
from weather_server.db.model import db, Device, Weather, DeviceSchema
from flask_testing import TestCase

import unittest
import warnings
import json
import os

# self.client will access the initialized app

devices_schema = DeviceSchema(many=True)

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

    def test_create_valid_device(self):
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "4321",
            "password": "12345678"
        })
        self.assert200(response, "Incorrect Response Code")

        # get last device
        new_dev = Device.query.order_by(Device.id.desc()).first()

        self.assertEqual(new_dev.latitude, 1234, "Latitude not set correctly")
        self.assertEqual(new_dev.longitude, 4321, "Latitude not set correctly")
        self.assertEqual(new_dev.password, "12345678", "Password not set correctly")

        response = self.client.get("/devices")

        self.assertEqual(devices_schema.dump([new_dev]),
                         devices_schema.load(response.json),
                         "New device not returned")

    def test_create_multiple_valid_devices(self):
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "4321",
            "password": "12345678"
        })
        self.assert200(response, "Incorrect Response Code")

        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "4321",
            "password": "12345678"
        })
        self.assert200(response, "Incorrect Response Code")


        response = self.client.get("/devices")

        devices = Device.query.all()

        self.assertEqual(2, len(devices))
        self.assertEqual(devices_schema.dump(devices),
                         devices_schema.load(response.json))

    def test_create_device_with_invalid_latitude(self):
        # try with letter and number
        response = self.client.post("/devices", data={
            "latitude": "1234a",
            "longitude": "4321",
            "password": "12345678"
        })
        self.assert400(response, "Incorrect Response Code")

        # try empty
        response = self.client.post("/devices", data={
            "latitude": "",
            "longitude": "4321",
            "password": "12345678"
        })
        self.assert400(response, "Incorrect Response Code")

        # try space only
        response = self.client.post("/devices", data={
            "latitude": "  ",
            "longitude": "4321",
            "password": "12345678"
        })
        self.assert400(response, "Incorrect Response Code")

        # try letters only
        response = self.client.post("/devices", data={
            "latitude": "abc",
            "longitude": "4321",
            "password": "12345678"
        })
        self.assert400(response, "Incorrect Response Code")


        devices = Device.query.all()

        self.assertEqual(0, len(devices))
        self.assertEqual([], devices)

        response = self.client.get("/devices")

        devices = Device.query.all()

        self.assertEqual(0, len(devices))
        self.assertEqual([], response.json)

    def test_create_device_with_invalid_longitude(self):
        # try with letter and number
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "4321a",
            "password": "12345678"
        })
        self.assert400(response, "Incorrect Response Code")

        # try empty
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "",
            "password": "12345678"
        })
        self.assert400(response, "Incorrect Response Code")

        # try space only
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "  ",
            "password": "12345678"
        })
        self.assert400(response, "Incorrect Response Code")

        # try letters only
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "abc",
            "password": "12345678"
        })
        self.assert400(response, "Incorrect Response Code")


        devices = Device.query.all()

        self.assertEqual(0, len(devices))
        self.assertEqual([], devices)

        response = self.client.get("/devices")

        devices = Device.query.all()

        self.assertEqual(0, len(devices))
        self.assertEqual([], response.json)

    def test_create_device_with_invalid_password(self):
        # try with letters and spaces
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "4321",
            "password": "1234567   "
        })
        self.assert400(response, "Incorrect Response Code")

        # try empty
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "4321",
            "password": ""
        })
        self.assert400(response, "Incorrect Response Code")

        # try space only
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "4321",
            "password": "   "
        })
        self.assert400(response, "Incorrect Response Code")

        devices = Device.query.all()

        self.assertEqual(0, len(devices))
        self.assertEqual([], devices)

        response = self.client.get("/devices")

        devices = Device.query.all()

        self.assertEqual(0, len(devices))
        self.assertEqual([], response.json)

    def test_delete_nonexistent_device(self):
        response = self.client.delete("/devices/0")
        self.assert404(response)

        response = self.client.delete("/devices/1")
        self.assert404(response)

        response = self.client.delete("/devices/-1")
        self.assert404(response)

    def test_delete_device_valid_password(self):
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "4321",
            "password": "12345678"
        })

        self.assert200(response, "Incorrect Response Code")

        devices = Device.query.all()

        self.assertEqual(1, len(devices))

        response = self.client.delete("/devices/1", headers={
            "password" : "12345678"
        })

        self.assert200(response, "Incorrect Response Code")

        devices = Device.query.all()

        self.assertEqual(0, len(devices))

    def test_delete_device_invalid_password(self):
        response = self.client.post("/devices", data={
            "latitude": "1234",
            "longitude": "4321",
            "password": "12345678"
        })

        self.assert200(response, "Incorrect Response Code")

        devices = Device.query.all()

        self.assertEqual(1, len(devices))

        response = self.client.delete("/devices/1", headers={
            "password" : "mysecretpass"
        })

        self.assert401(response, "Incorrect Response Code")

        devices = Device.query.all()

        self.assertEqual(1, len(devices))

class TestFrontEndViews(WeatherServerBase):

    def test_home_template_used(self):
        response = self.client.get("/")
        self.assert_template_used("index.html")

    def test_mainjs_used(self):
        warnings.simplefilter("ignore", ResourceWarning)

        response = self.client.get("/static/main.js")

        jsfile = open(os.path.join(os.getcwd(),
                                   os.path.dirname(__file__),
                                   "static",
                                   "main.js"), "r")

        jscontent = jsfile.read()
        jsfile.close()

        self.assertEqual(jscontent, response.data.decode('utf-8'))

    def test_jqueryjs_used(self):
        warnings.simplefilter("ignore", ResourceWarning)

        response = self.client.get("/static/jquery-3.2.1.min.js")

        jsfile = open(os.path.join(os.getcwd(),
                                   os.path.dirname(__file__),
                                   "static",
                                   "jquery-3.2.1.min.js"), "r")
        jscontent = jsfile.read()
        jsfile.close()

        self.assertEqual(jscontent, response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
