from sqlalchemy.orm import backref
from . import db
from flask_login import UserMixin
import datetime as dt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)
    contacts = db.relationship('Contact', backref='user', lazy=True)
    

    def __repr__(self):
        return '<User %r>' % self.email


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    complete = db.Column(db.Boolean(), nullable=False, default=False)
    date_created = db.Column(db.DateTime, default=dt.datetime.now())
    due_date = db.Column(db.DateTime, default=dt.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return '<Todo %r>' % self.id

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employer = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    date_applied = db.Column(db.DateTime, default=dt.datetime.now())
    platform = db.Column(db.String(250), nullable=False)
    remote = db.Column(db.Boolean(), nullable=False, default=False)
    salary = db.Column(db.String(250), nullable=True)
    point_of_contact = db.Column(db.String(250), nullable=True)
    comments = db.Column(db.String(5000), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return '<Contact %r>' % self.id





