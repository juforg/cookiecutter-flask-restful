from flask import Flask, request, session
import logging, logging.config, yaml, os, time
from {{cookiecutter.app_name}} import api
from {{cookiecutter.app_name}} import auth
from {{cookiecutter.app_name}}.extensions import apispec
from {{cookiecutter.app_name}}.extensions import db
from {{cookiecutter.app_name}}.extensions import jwt
from {{cookiecutter.app_name}}.extensions import migrate

{%- if cookiecutter.use_celery == "yes"%}, celery{% endif%}

logger = logging.getLogger(__name__)

def create_app(testing=False):
    """Application factory, used to create application
    """
    init_logger()
    app = Flask("{{cookiecutter.app_name}}")
    app.config.from_object("{{cookiecutter.app_name}}.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)
    init_around_request(app)
{%- if cookiecutter.use_celery == "yes" %}
    init_celery(app)
{%- endif %}
{%- if cookiecutter.use_redis == "yes" %}
    redis_client.init_app(app=app)
{%- endif %}
    return app


def init_logger():
    with open('logging.yml', 'r') as f_conf:
        dict_conf = yaml.load(f_conf, Loader=yaml.FullLoader)
    log_path = os.getenv("LOG_PATH")
    if log_path:
        # log_path2 = log_path.replace('{{cookiecutter.app_name}}.log', '{{cookiecutter.app_name}}.log')
        dict_conf["handlers"]["all_file_handler"]["filename"] = log_path
    else:
        dict_conf["handlers"]["all_file_handler"]["filename"] = "./tmp/logs/{{cookiecutter.app_name}}.log"
    logging.config.dictConfig(dict_conf)


def configure_extensions(app):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)
{%- if cookiecutter.use_excel == "yes" %}
    flask_excel.init_excel(app)
{%- endif %}


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme("jwt", {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    })
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.error_handler.err_bp)
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(api.resources.user.user_bp)
    app.register_blueprint(api.resources.dict.dict_bp)
{%- if cookiecutter.use_celery == "yes" %}


def init_celery(app=None):
    app = app or create_app()
    # celery.conf.beat_schedule = {
    #     'dummy_task': {
    #         'task': '{{cookiecutter.app_name}}.tasks.example.dummy_task',
    #         'schedule': crontab(minute=10, hour=2)
    #     }
    # }
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
{%- endif %}


def init_around_request(app):
    @app.before_request
    def before_request():
        session['req_start_time'] = time.time()
        pass

    @app.after_request
    def after_request(response):
        logger.info("[performance]接口请求:, %s, 耗时:, %s", request.url, time.time() - session['req_start_time'])
        return response
        pass
