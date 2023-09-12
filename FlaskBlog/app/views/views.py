# -*- coding:utf-8 -*-

from flask import Blueprint,render_template
from app import db
bp = Blueprint('blog',__name__,url_prefix='/blog')


@bp.route('/index')
def index():
    db.create_all()
    return 'hello world'
