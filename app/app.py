from flask import Flask
from flask import render_template
from app.extensions import db, login


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.secret_key = 'xyz'
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    login.init_app(app)


app = create_app()
