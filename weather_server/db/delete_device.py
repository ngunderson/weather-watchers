from model import db, Weather, Device
from weather_server.server import create_app

create_app().app_context().push()

dev = Device.query.get(1)

db.session.delete(dev)
db.session.commit()
