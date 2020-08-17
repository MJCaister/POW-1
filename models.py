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


class Capture(db.Model):
    __tablename__ = 'Capture'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text, nullable=False)
    fulldate = db.Column(db.Text)
    desc = db.Column(db.Text)


class Prisoner(db.Model):
    __tablename__ = 'Prisoner'

    id = db.Column(db.Integer, primary_key=True)
    service_number = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.ForeignKey('Rank.id'))
    surname = db.Column(db.Text, nullable=False)
    initial = db.Column(db.Text)
    capture = db.Column(db.ForeignKey('Capture.id'))
    first_names = db.Column(db.Text)
    branch = db.Column(db.Text)
    photo = db.Column(db.String)

    Capture = db.relationship('Capture', primaryjoin='Prisoner.capture == Capture.id', backref='prisoners')
    Rank = db.relationship('Rank', primaryjoin='Prisoner.rank == Rank.id', backref='prisoners')
    units = db.relationship('PrisonerUnit', back_populates='prisoner')


class PrisonerUnit(db.Model):
    __tablename__ = 'PrisonerUnit'

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.ForeignKey('Prisoner.id'))
    uid = db.Column(db.ForeignKey('Unit.id'))

    prisoner = db.relationship('Prisoner', back_populates="units")
    unit = db.relationship('Unit', back_populates="prisoners")


class Rank(db.Model):
    __tablename__ = 'Rank'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    initial = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text)


class Unit(db.Model):
    __tablename__ = 'Unit'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    fullname = db.Column(db.Text)
    desc = db.Column(db.Text)
    photo = db.Column(db.String)

    prisoners = db.relationship('PrisonerUnit', back_populates="unit")


class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(64))
    email = db.Column(db.Text(120))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Comment(db.Model):
    __tablename__ = 'Comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500))
    userid = db.Column(db.ForeignKey('User.id'))
    powid = db.Column(db.ForeignKey('Prisoner.id'))

    #forgein key many to one relationships
    User = db.relationship('User', primaryjoin='Comment.userid == User.id', backref='comments')
    Prisoner = db.relationship('Prisoner', primaryjoin='Comment.powid == Prisoner.id', backref='comments')


class UserPrisoner(db.Model):
    __tablename__ = 'UserPrisoner'

    id = db.Column(db.Integer, primary_key=True)
    powid = db.Column(db.ForeignKey('Prisoner.id'))
    userid = db.Column(db.ForeignKey('User.id'))

    Prisoner = db.relationship('Prisoner', primaryjoin='UserPrisoner.powid == Prisoner.id', backref='users')
    User = db.relationship('User', primaryjoin='UserPrisoner.userid == User.id', backref='prisoners')
