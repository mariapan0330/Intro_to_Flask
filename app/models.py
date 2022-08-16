from app import db
from datetime import datetime

class User(db.Model):
    # This is where you are creating a table like in SQL
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
                                                            # This makes datetime default to now (must import datetime)