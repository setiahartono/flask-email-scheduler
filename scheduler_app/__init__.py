# import os

from celery import Celery
from flask import Flask
from flask_admin import Admin
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from . import celeryconfig


app = Flask(__name__)
app.config.from_object('scheduler_app.config')

db = SQLAlchemy(app)
admin = Admin(app, name='Dashboard')


def make_celery(app):
    # create context tasks in celery
    celery = Celery(
        app.import_name,
        broker=app.config['BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(app)
mail = Mail(app)
