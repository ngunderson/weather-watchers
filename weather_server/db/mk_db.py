from weather_server.db.model import db
from weather_server.server import create_app
create_app().app_context().push()

# Script to create initial SQLite DB
#print 'Uncomment this file to create a new db based on model.py'
#db.create_all()
