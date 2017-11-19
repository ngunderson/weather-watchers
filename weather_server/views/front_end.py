from flask import Blueprint, render_template
from weather_server.db.model import Device

front_end = Blueprint("front_end", __name__)

@front_end.route("/", methods=["GET"])
def home():
    """
    Returns the base html template
    """

    return render_template("index.html")
