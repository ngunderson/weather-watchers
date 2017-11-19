from flask import Flask
from weather_server.db.model import db, ma
from weather_server.views.front_end import front_end
from weather_server.views.api import api

import logging
import sys

# intialize application for use database

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/weather.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    ma.init_app(app)
    return app

##### Logging config #####
#logging.basicConfig(filename="server.log", level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

##### Run the application #####

def main():
    app = create_app()
    app.register_blueprint(front_end)
    app.register_blueprint(api)
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
