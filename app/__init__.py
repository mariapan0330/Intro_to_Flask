from flask import Flask

app1 = Flask(__name__) 
# if you do app = Flask(__name__, render_name="abc123") then it will look for a folder called abc123 instead of 'templates'

from . import routes

