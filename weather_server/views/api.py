from flask import Flask, request, jsonify, Blueprint
from weather_server.db.model import db, Device, Weather, DeviceSchema, WeatherSchema

api = Blueprint("api", __name__)

SUCCESS = "", 200
BAD_REQUEST = "", 400
UNAUTHORIZED= "", 401

##### Initialize Schemas used to format return data #####

device_schema = DeviceSchema(many=True)
weather_schema = WeatherSchema(many=True)

@api.route("/devices", methods=["POST"])
def create_device():
    try:
        # verify data
        dev_lat = float(request.form["latitude"])
        dev_long = float(request.form["longitude"])
        dev_password = request.form["password"]
        if dev_password.strip() is "" or len(dev_password) < 8:
            raise Exception
    except Exception:
        return "", 400

    new_dev = Device(
        latitude=dev_lat,
        longitude=dev_long,
        password=dev_password
    )
    db.session.add(new_dev)
    db.session.commit()


    return "", 200

@api.route("/devices/<dev_id>", methods=["DELETE"])
def delete_device(dev_id):
    dev = Device.query.get(dev_id)
    if dev is None:
        return "", 400

    print("HEADERS are " + str(request.headers))
    if dev.password != request.headers.get("password"):
        return "", 401

    db.session.delete(dev)
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
