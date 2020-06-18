from flask.cli import load_dotenv
from {{cookiecutter.app_name}}.app import init_celery

load_dotenv()
app = init_celery()
app.conf.imports = app.conf.imports + ('{{cookiecutter.app_name}}.tasks',)
