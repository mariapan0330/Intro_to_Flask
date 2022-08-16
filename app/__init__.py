from flask import Flask

app = Flask(__name__) 
app.config["SECRET_KEY"] = 'you-will-never-guess'
# if you do app = Flask(__name__, render_name="abc123") then it will look for a folder called abc123 instead of 'templates'

from . import routes

