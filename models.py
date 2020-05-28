# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Capture(db.Model):
    __tablename__ = 'Capture'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text)



#t_Get Distinct Values for fixing data = db.Table(
#    'Get Distinct Values for fixing data',
#    db.Column('NULL', db.NullType)
#)



class Prisoner(db.Model):
    __tablename__ = 'Prisoner'

    id = db.Column(db.Integer, primary_key=True)
    service_number = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.ForeignKey('Rank.id'))
    surname = db.Column(db.Text, nullable=False)
    initial = db.Column(db.Text)
    capture = db.Column(db.ForeignKey('Capture.id'))

    Capture = db.relationship('Capture', primaryjoin='Prisoner.capture == Capture.id', backref='prisoners')
    Rank = db.relationship('Rank', primaryjoin='Prisoner.rank == Rank.id', backref='prisoners')
    Unit = db.relationship('Unit', secondary='PrisonerUnit', backref='prisoners')



t_PrisonerUnit = db.Table(
    'PrisonerUnit',
    db.Column('pid', db.ForeignKey('Prisoner.id')),
    db.Column('uid', db.ForeignKey('Unit.id'))
)



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
    desc = db.Column(db.Text)
    photo = db.Column(db.Numeric)



#t_sqlite_sequence = db.Table(
#    'sqlite_sequence',
#    db.Column('name', db.NullType),
#    db.Column('seq', db.NullType)
#)
