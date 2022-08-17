from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# from the confg module we made, import the config class we made.
# We'll use this to set attributes here.

app = Flask(__name__) 
# if you do app = Flask(__name__, render_name="abc123") then it will look for a folder called abc123 instead of 'templates'

# app.config["SECRET_KEY"] = 'you-will-never-guess'
# ^ instead of that, we'll generate a secret key and other configurations from our Config class
app.config.from_object(Config)

# Create an instance of SQLAlchmey (the ORM) with the Flask Application:
db = SQLAlchemy(app)

# pass app and db into migration engine
migrate = Migrate(app, db)

# Create an instance of the loginManager to handle authentication
login = LoginManager(app)

from . import routes, models