from flask import Flask, request, jsonify, Blueprint
from weather_server.db.model import db, Device, Weather, DeviceSchema, WeatherSchema

api = Blueprint("api", __name__)

##### Initialize Schemas used to format return data #####

device_schema = DeviceSchema(many=True)
weather_schema = WeatherSchema(many=True)

@api.route("/devices", methods=["POST"])
def create_device():
    try:
        dev_lat = float(request.form["latitude"])
        dev_long = float(request.form["longitude"])
    except Exception:
        return "", 400

    new_dev = Device(
        latitude=dev_lat,
        longitude=dev_long
    )
    db.session.add(new_dev)
    db.session.commit()


    return "", 200

@api.route("/devices", methods=["GET"])
def get_devices():
    """
    Returns all the devices
    """
    devices = Device.query.all()
    result = device_schema.dump(devices)
    return jsonify(result.data)
