import click
from flask.cli import FlaskGroup

from {{cookiecutter.app_name}}.app import create_app
from tests.generator import model_generator

def create_{{cookiecutter.app_name}}(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_{{cookiecutter.app_name}})
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables
    and create a new user named admin with password admin
    """
    from {{cookiecutter.app_name}}.extensions import db
    from {{cookiecutter.app_name}}.models import User
    click.echo("create database")
    db.create_all()
    click.echo("done")

    click.echo("create user")
    user = User(
        username="{{cookiecutter.admin_user_username}}",
        email="{{cookiecutter.admin_user_email}}",
        password="{{cookiecutter.admin_user_password}}",
        active=True
    )
    db.session.add(user)
    # db.session.flush()
    click.echo("created user admin")

@cli.command("generagte_model")
def generagte_model():
    click.echo("start generagte models")
    model_generator.start()
    click.echo("finish !!!")

if __name__ == "__main__":
    cli()
