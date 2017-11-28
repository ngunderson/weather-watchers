#!/usr/bin/env python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

##### Models #####

class Device(db.Model):
    __tablename__ = "device"
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float(precision=6), nullable=False, unique=False)
    longitude = db.Column(db.Float(precision=6), nullable=False, unique=False)
    weather = db.relationship("Weather", backref="Device")
    # restricts device deletion
    password = db.Column(db.String(100), nullable=False)


class Weather(db.Model):
    __tablename__ = "weather"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    temp = db.Column(db.Integer, nullable=True)
    # new columns would have to be added for new weather data

##### SCHEMAS #####

class WeatherSchema(ma.Schema):
    class Meta:
        fields = ("time", "temp")

class DeviceSchema(ma.Schema):
    class Meta:
        fields = ("id", "latitude", "longitude", "weather")

    weather = ma.Nested(WeatherSchema, many=True)
