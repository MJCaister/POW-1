# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Capture(db.Model):
    __tablename__ = 'Capture'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text)



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
    desc = db.Column(db.Text)
    photo = db.Column(db.Numeric)

    prisoners = db.relationship('PrisonerUnit', back_populates="unit")

#t_sqlite_sequence = db.Table(
#    'sqlite_sequence',
#    db.Column('name', db.NullType),
#    db.Column('seq', db.NullType)
#)
