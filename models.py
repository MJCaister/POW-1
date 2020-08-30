# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Table, Text, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt
from routes import app

db = SQLAlchemy()


# Capture table, has one to many relationship with Prisoner table
class Capture(db.Model):
    __tablename__ = 'Capture'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text, nullable=False)
    fulldate = db.Column(db.Text)
    desc = db.Column(db.Text)


# Prisoner table
class Prisoner(db.Model):
    __tablename__ = 'Prisoner'

    id = db.Column(db.Integer, primary_key=True)
    service_number = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.ForeignKey('Rank.id'))
    surname = db.Column(db.Text, nullable=False)
    initial = db.Column(db.Text)
    capture = db.Column(db.ForeignKey('Capture.id'))
    first_names = db.Column(db.Text)
    photo = db.Column(db.String)

    # many to one relationship with Capture table
    Capture = db.relationship('Capture', primaryjoin='Prisoner.capture == Capture.id', backref='prisoners')
    # many to one relationship with Rank table
    Rank = db.relationship('Rank', primaryjoin='Prisoner.rank == Rank.id', backref='prisoners')
    # Many to many relationship with Unit table
    units = db.relationship('PrisonerUnit', back_populates='prisoner')


# intermediate table for Prisoner and Unit many to many relationship
class PrisonerUnit(db.Model):
    __tablename__ = 'PrisonerUnit'

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.ForeignKey('Prisoner.id'))
    uid = db.Column(db.ForeignKey('Unit.id'))

    prisoner = db.relationship('Prisoner', back_populates="units")
    unit = db.relationship('Unit', back_populates="prisoners")


# Rank table, has one to many relationship with Prisoner
class Rank(db.Model):
    __tablename__ = 'Rank'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    initial = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text)


# Unit table
class Unit(db.Model):
    __tablename__ = 'Unit'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    fullname = db.Column(db.Text)
    desc = db.Column(db.Text)
    photo = db.Column(db.String)

    # Has many to many relationship with Unit table
    prisoners = db.relationship('PrisonerUnit', back_populates="unit")


# User table
class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(64))
    email = db.Column(db.Text(120))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Sets the password hash that's stored in the db
    def set_password(self, password):
        # password is salted (8 length) and hashed using sha256
        self.password_hash = generate_password_hash(password)

    # generates password hash and checks it against hash stored in db
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # generates a token to be emailed to the user if they forget their password
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # this decodes the token that's emailed
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


# Comment table
class Comment(db.Model):
    __tablename__ = 'Comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500))
    userid = db.Column(db.ForeignKey('User.id'))
    powid = db.Column(db.ForeignKey('Prisoner.id'))

    # forgein key many to one relationships
    User = db.relationship('User', primaryjoin='Comment.userid == User.id', backref='comments')
    Prisoner = db.relationship('Prisoner', primaryjoin='Comment.powid == Prisoner.id', backref='comments')


# Following table
class Following(db.Model):
    __tablename__ = 'Following'

    id = db.Column(db.Integer, primary_key=True)
    powid = db.Column(db.ForeignKey('Prisoner.id'))
    userid = db.Column(db.ForeignKey('User.id'))

    # foreign key many to one relationships to connect the user and prisoner
    User = db.relationship('User', primaryjoin='Following.userid == User.id', backref='followers')
    Prisoner = db.relationship('Prisoner', primaryjoin='Following.powid == Prisoner.id', backref='followers')
