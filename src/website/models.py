from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    retweets = db.relationship('User', secondary='retweets', backref=db.backref('retweeted_notes', lazy='dynamic'))

# Create a join table for the retweets relationship
retweets = db.Table('retweets',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True)
)
class UserFollows(db.Model):
    __tablename__ = 'user_follows'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_followed = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    notes = db.relationship('Note', backref='user')

    # Define the relationship to the users the current user follows
    followed_users = db.relationship('User',
                                     secondary='user_follows',
                                     primaryjoin=(id == UserFollows.follower_id),
                                     secondaryjoin=(id == UserFollows.followed_id),
                                     backref=db.backref('followers', lazy='dynamic'),
                                     lazy='dynamic')


