from pickle_ import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///app.db"
db=SQLAlchemy(app)

from . import user