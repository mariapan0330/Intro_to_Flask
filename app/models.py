from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash as gph
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

    def __init__(self, **kwargs):
        # has to have kwargs ability and call super with the kwargs
        super().__init__(**kwargs)
        self.password = gph(kwargs['password'])
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f"<User {self.user_id} | {self.username}>"


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # making a foreign key like in SQL: FOREIGN KEY(user_id) REFERENCES user(user_id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f"<User {self.post_id} | {self.title}>"