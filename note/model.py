from datetime import datetime
import pytz
from note import db


def get_lithuanian_time():
    lithuanian_tz = pytz.timezone('Europe/Vilnius')
    return datetime.now(lithuanian_tz)


class NoteEntry(db.Model):
    __tablename__ = 'note_entry'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    topic = db.Column(db.String(20), nullable=False)
    created = db.Column(db.TIMESTAMP, default=get_lithuanian_time, nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='note_entries')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    note_entries = db.relationship('NoteEntry', back_populates='user')
