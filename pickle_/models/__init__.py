from pickle_ import app,login
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///app.db"
db=SQLAlchemy(app)
migrate=Migrate(app,db)

from . import user
