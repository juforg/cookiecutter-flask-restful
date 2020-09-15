from {{cookiecutter.app_name}}.app import create_app
from flask.cli import load_dotenv

load_dotenv()
app = create_app()
