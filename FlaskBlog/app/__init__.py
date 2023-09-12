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

    from .admin import admin
    app.register_blueprint(admin, url_prefix='/admin')
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    from .main import main
    app.register_blueprint(main, url_prefix='/main')

    mail = Mail(app)
    bootstrap = Bootstrap(app)

    return app


