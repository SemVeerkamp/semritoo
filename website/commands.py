import click
from flask.cli import with_appcontext

from website.extensions import db
from website.models import User, Prediction

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
