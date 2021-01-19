import click
from flask.cli import with_appcontext
from code_generator import model_generator

@click.group()
def cli():
    """Main entry point"""


@cli.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from {{cookiecutter.app_name}}.extensions import db
    from {{cookiecutter.app_name}}.models import User

    click.echo("create user")
    user = User(username="{{cookiecutter.admin_user_username}}", email="{{cookiecutter.admin_user_email}}", password="{{cookiecutter.admin_user_password}}", active=True)
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
