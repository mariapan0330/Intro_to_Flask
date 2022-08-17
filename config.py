import os

basedir = os.path.abspath(os.path.dirname(__file__))
# this will dynamically change with wherever you put it

class Config:
    # this generates a secret key or defaults to 'you will never guess' if that didn't work
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'you-will-never-guess'
    # 'get' methods will look for values from our environmental variables,
    # and will return a val or None.
    
    # If None, default to whatever is after the 'or'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False