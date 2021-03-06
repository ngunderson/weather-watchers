from flask import Flask
from weather_server.db.model import db, ma
from weather_server.views.front_end import front_end
from weather_server.views.api import api

import logging
import sys

CFG = {
    "SQLALCHEMY_DATABASE_URI" : "sqlite:////home/nate/workspace/weather-db/weather.db"
}


# intialize application for use database

def create_app(cfg=CFG):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['TESTING'] = cfg.get("TESTING") or False
    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(front_end)
    app.register_blueprint(api)
    return app

##### Logging config #####
#logging.basicConfig(filename="server.log", level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

##### Run the application #####

def main():
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
