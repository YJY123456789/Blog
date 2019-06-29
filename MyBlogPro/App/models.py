import random

from App.exts import db


# 分类
# class Person(db.Model):
    # id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # name = db.Column(db.String(20), unique=True)
    # age = db.Column(db.Integer, default=18)


class Sort(db.Model):
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String(100),unique=True)
    othername = db.Column(db.String(100),unique=True)
    num=db.Column(db.Integer)
    ars= db.relationship('Article', backref="s", lazy=True)

class Article(db.Model):
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String(200))
    content = db.Column(db.String(255))
    my_sort = db.Column(db.Integer,db.ForeignKey(Sort.id))
    pic = db.Column(db.Integer)


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(50))