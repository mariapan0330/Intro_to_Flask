# first, >>> (kek_venv) pip install flask-httpauth && pip freeze > requirements.txt
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from datetime import datetime

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password # this is a decorator method on the basic_auth class that gets the data from request headers.
# We set it up to either return the user if credentials match, or return None which will throw a 401 error for Unauthorized Access.
def verify(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password): # if the user is not None and the password is the one passed in, return user
        return user
    # if these fail it will return None by default

# now in blueprints > api > routes.py, we gotta set up the routes that use the verification


@token_auth.verify_token
def verify(token):
    user = User.query.filter_by(token=token).first()
    now = datetime.utcnow()
    if user and user.token_expiration > now: # is there a user with the current token and the token expires sometime that has not passed, you can return the user (otherwise, returns None)
        return user