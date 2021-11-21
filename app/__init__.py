import click
from flask import Flask
from app.extension import *
from app.model.dbmodel import *
from app.user import user
from app.file import file
from app.admin import admin
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_pyfile('setting.py')

    register_extensions(app)
    register_blueprint(app)
    register_command(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprint(app):
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(file, url_prefix='/file')
    app.register_blueprint(admin, url_prefix='/admin')


def register_command(app):
    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()
        user = User(user_name="123", avatar="312")
        admin = Admin(name="admin", password="123456")
        course = Course(title="1.初识Python", details="1.md")
        problem = Problem(
            details="Write a program which will find all such numbers which are divisible by 7 but are not a multiple of 5, between 2000 and 3200 (both included). The numbers obtained should be printed in a comma-separated sequence on a single line.",
            hint="Consider use range(#begin, #end) method",
            reference_code="1.py",
            level=1
        )
        db.session.add(user)
        db.session.add(admin)
        db.session.add(course)
        db.session.add(problem)
        db.session.commit()
        click.echo('create success')