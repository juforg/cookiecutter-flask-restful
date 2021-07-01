"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from flask_migrate import Migrate
{%- if cookiecutter.use_celery == "yes" %}
from celery import Celery
{%- endif %}
{%- if cookiecutter.use_redis == "yes" %}
from flask_redis import FlaskRedis
{%- endif %}
{%- if cookiecutter.use_apispec == "yes"%}
from {{cookiecutter.app_name}}.commons.apispec import APISpecExt {% endif%}


db = SQLAlchemy(session_options={'autocommit': True})
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
{%- if cookiecutter.use_apispec == "yes"%}
apispec = APISpecExt() {% endif%}
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
{%- if cookiecutter.use_celery == "yes" %}
celery = Celery()
{%- endif %}
{%- if cookiecutter.use_redis == "yes" %}
redis_client = FlaskRedis()
{%- endif %}

# Marshmallow default message coverage
fields.Field.default_error_messages["required"] = "必填项没值"
fields.Field.default_error_messages["null"] = "字段不可以为null"
fields.Field.default_error_messages["validator_failed"] = "值无效"
fields.Integer.default_error_messages = {"invalid": "不是一个有效的整数"}
validate.Length.message_min = "字段长度不允许小于最小长度 {min}"
validate.Length.message_max = "字段长度不允许超过最大长度{max}"
validate.Length.message_all = "字段长度必须大于 {min} 小于 {max}"
validate.Length.message_equal = "字段长度必须为 {equal}"
validate.Range.message_min = "必须 {min_op} \{\{min\}\}."
validate.Range.message_gte = "大于等于"
validate.OneOf.default_message = "值必须是其中一个: {choices}."
