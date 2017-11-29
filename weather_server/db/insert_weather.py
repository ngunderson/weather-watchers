from weather_server.db.model import db, Weather
from weather_server.server import create_app

from datetime import datetime, timezone
from dateutil import tz

create_app().app_context().push()

# This file serves as a reference USP for the SQLite DB

weather = Weather(
    device_id=1,
    time=datetime.utcnow(),
    temp=60
)

db.session.add(weather)
db.session.commit()
