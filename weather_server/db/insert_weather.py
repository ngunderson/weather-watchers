from model import db, Weather
from weather_server.server import create_app

from datetime import datetime, timezone
from dateutil import tz

create_app().app_context().push()

to_zone = tz.gettz("CST")

weather = Weather(
    device_id=1,
    time=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(to_zone),
    temp=60
)

db.session.add(weather)
db.session.commit()
