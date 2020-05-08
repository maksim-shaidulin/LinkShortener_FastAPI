# python mograte.py db init
# python mograte.py db migrate
# python mograte.py db upgrade

# from flask import Flask
# from marshmallow import Schema, fields, pre_load, validate
from marshmallow import fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import random
import string

ma = Marshmallow()
db = SQLAlchemy()


class Link(db.Model):
    __tablename__ = 'links'
    short_link_length = 6
    letters = string.ascii_letters + string.digits
    short_link = db.Column(
        db.String(short_link_length),
        nullable=False, primary_key=True)
    full_link = db.Column(db.String(500), nullable=False)
    created = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(),
        nullable=False)

    def __init__(self, full_link):
        self.full_link = full_link
        self.short_link = self.generate_short_link(full_link)

    def generate_short_link(self, link) -> str:
        return ''.join(random.choice(self.letters)
                       for _ in range(self.short_link_length))


class LinkSchema(ma.Schema):
    full_link = fields.String(required=True)
    short_link = fields.String()
    created = fields.DateTime()


"""
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(),
        nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id', ondelete='CASCADE'), nullable=False)
    category = db.relationship(
        'Category', backref=db.backref('comments', lazy='dynamic'))

    def __init__(self, comment, category_id):
        self.comment = comment
        self.category_id = category_id


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class CategorySchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class CommentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    category_id = fields.Integer(required=True)
    comment = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()
"""
