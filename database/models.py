# coding: utf-8
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Json(db.Model):
    __tablename__ = 'Json'

    key = db.Column(db.String(32), nullable=False)
    value = db.Column(db.String(128))
    index = db.Column(db.Integer, primary_key=True)


class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String(255, 'utf8_bin'), primary_key=True)
    password = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    type = db.Column(db.String(255, 'utf8_bin'), nullable=False)
