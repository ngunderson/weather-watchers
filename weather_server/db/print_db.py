#!/usr/bin/env python
# This is an example file that includes a number of potential
# interactions with a sqlite databse with SQLAlchemy
#
# Author : Nate Gunderson <gundersonn@uwplatt.edu>

from sqlalchemy import create_engine, inspect, Table, MetaData
from model import Device, Weather, db
from ... import app

app.app_context().push()

print("devices:\n")
for device in Device.query.all():
    print("id: {}, latitude: {} longitude: {} weather: {}").format(
        device.id, device.latitude, device.longitude, device.weather
    )

print("weather data:\n")
for weather in Weather.query.all():
    print("Id: {}\n device id: {}\n  time: {}\n temp: {}\n key: {}\n").format(
        weather.id, weather.device_id, weather.time, weather.temp, weather.key
    )
