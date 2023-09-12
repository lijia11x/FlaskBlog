# -*- coding:utf-8 -*-
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_session import Session
# db = SQLAlchemy()
from flask_mail import Mail
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.Config')
    mail = Mail(app)
    bootstrap = Bootstrap(app)
    from .admin import admin
    app.register_blueprint(admin, url_prefix='/admin')



    return app


