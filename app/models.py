from app import db, login
import base64 # lets you convert time to stuff
from datetime import datetime, timedelta # DATETIME lets you create a timestamp right now; TIMEDELTA lets you calculate time differences
import os # lets you work with the user's computer
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # This is where you are creating a table like in SQL
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
                                                            # This makes datetime default to now (must import datetime)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # The 'dynamic' in lazy means that it will /first/ apply whatever filter you need  /then/ search through those, instead of searching through everything with the filter (or something)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime) # token and token_exp don't work (they're NULL) without a get_token() method below
    # when we change the database, do the following in the terminal to reflect those changes in the sqlite database:
    # >>> flask db migrate -m "message"
    # >>> flask db upgrade

    def __init__(self, **kwargs):
        # has to have kwargs ability and call super with the kwargs
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f"<User {self.user_id} | {self.username}>"
    

    def check_password(self, pw):
        # returns true if self.password == the password they put in
        return cph(self.password, pw)

    def set_password(self, pw):
        self.password = gph(pw)
    
    def get_id(self):
        return str(self.user_id)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'date_created': self.date_created
        }


    def get_token(self, expires_in=300): # import base64; from datetime import datetime, timedelta; import os
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token
    

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        db.session.commit()



@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # making a foreign key like in SQL: FOREIGN KEY(id) REFERENCES user(id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f"<User {self.post_id} | {self.title}>"
    
    def update(self, **kwargs):
        for key, val in kwargs.items():
            if key in {'title', 'body'}:
                setattr(self, key, val)
        db.session.commit() # so the database changes as well 

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.post_id,
            'title': self.title,
            'body': self.body,
            'date_created': self.date_created,
            'user_id': self.user_id,
        }