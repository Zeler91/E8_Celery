from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@db:5432/find_python"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
celery = Celery(app.name, broker='redis://redis')
celery.conf.update(result_expires = 3600)

from app import models, views
db.create_all()