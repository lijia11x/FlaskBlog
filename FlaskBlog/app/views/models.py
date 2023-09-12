# -*- coding:utf-8 -*-
from app import db
from datetime import datetime


class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),nullable=False)
    icon = db.Column(db.String(128),nullable=True)
    add_date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    pub_date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow, onupdate=datetime.utcnow,)

    def __repr__(self):
        return '<Category %r>' % self.name



