"""Default configuration

Use env var to override
"""
import os, datetime
from marshmallow import fields, validate
from sqlalchemy.pool import QueuePool

ENV = os.getenv("FLASK_ENV")
# DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")
PROPAGATE_EXCEPTIONS = True
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_BINDS = {
#     'transfer_db': os.getenv("SQLALCHEMY_BINDS_TRANSFER")
# }
# 如果设置为Ture， SQLAlchemy 会记录所有 发给 stderr 的语句，这对调试有用。(打印sql语句)#sql 日志
SQLALCHEMY_ECHO = True if os.getenv("SQLALCHEMY_ECHO") == "True" else False
# 如果为True，则连接池将记录信息输出，例如连接失效时以及连接被回收到默认日志处理程序时，默认sys.stdout为输出。如果设置为字符串 "debug"，则日志记录将包括池检出和签入。使用标准Python logging模块也可以直接控制日志记录
# SQLALCHEMY_ECHO_POOL = True if os.getenv("SQLALCHEMY_ECHO_POOL") == "True" else False
# 默认2小时。该值一定要比数据库wait_timeout小，否则它不起作用
# SQLALCHEMY_POOL_RECYCLE = 3000
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': int(os.getenv("SQLALCHEMY_POOL_SIZE", 0)),
    'max_overflow': int(os.getenv("SQLALCHEMY_POOL_OVERFLOW", 2)),
    'echo_pool': 'debug' if os.getenv("SQLALCHEMY_ECHO_POOL") == "True" else False,
    'pool_recycle': 60 * 5,
    'pool_timeout': int(os.getenv("SQLALCHEMY_POOL_TIMEOUT", 20)),
    'pool_pre_ping': True,   # 测试是否可用
    'pool_use_lifo': False,   # 越老的越容易被回收，一定要跟ping 配合，否则老的极易被回收造成连接不可用
    'poolclass': QueuePool,  # flask 应用可以设QueuePool，celery应用可能不用池
    'isolation_level': 'AUTOCOMMIT',
    'connect_args': {'ssl': {'ca': None}}  #开启ssl连接的数据库配置
}
JWT_SECRET_KEY = SECRET_KEY
JWT_BLACKLIST_ENABLED = False
# JWT_IDENTITY_CLAIM = 'identity'
# JWT_USER_CLAIMS = 'user_claims'
# JWT_ALGORITHM = 'HS512'
# JWT_DECODE_ALGORITHMS = ['HS256', 'HS512']
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_TOKEN_LOCATION = ('headers', 'cookies')
JWT_COOKIE_CSRF_PROTECT = False if os.getenv("JWT_COOKIE_CSRF_PROTECT") == "False" else True
JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", '120')))
{%- if cookiecutter.use_celery == "yes" %}
# ------------------------------------------------CELERY START-----------------
# 修改默认队列名，防止不同应用使用同个broker出现问题
CELERY_TASK_DEFAULT_QUEUE = os.getenv("CELERY_TASK_DEFAULT_QUEUE", "{{cookiecutter.app_name}}_default_q")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND_URL")
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁
CELERY_IGNORE_RESULT = True   # 任务结果不缓存
# CELERY_TASK_SERIALIZER = 'pickle'  # 任务序列化和反序列化使用pickle方案
CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用可读性更好的json
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'pickle']  # 指定接收的内容类型
# C_FORCE_ROOT = 'true'  # 允许root用户启动celery
# CELERYD_CONCURRENCY = 1  # 并发只有一个进程消费
# CELERYD_PREFETCH_MULTIPLIER = 1
# worker_max_memory_per_child = int(celery_max_mem_kilobytes / app.conf.worker_concurrency)
CELERYD_MAX_TASKS_PER_CHILD = 10        # 每个worker最多执行万10个任务就会被销毁，可防止内存泄露
CELERY_TASK_RESULT_EXPIRES = 60 * 10  # 任务结果过期时间
CELERYD_TASK_TIME_LIMIT = 60 * 60 * 2  # 任务超时时间
CELERYD_HIJACK_ROOT_LOGGER = True  # ：默认true，先前所有的logger的配置都会失效，可以通过设置false禁用定制自己的日志处理程序；
# CELERYD_TASK_LOG_FORMAT ="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
CELERYD_TASK_LOG_FORMAT = "%(asctime)s %(levelname)s <PID %(process)d:%(processName)s> %(name)s.%(funcName)s(): %(message)s"
CELERYD_LOG_FORMAT = "%(asctime)s %(levelname)s <PID %(process)d:%(processName)s> %(name)s.%(funcName)s(): %(message)s"
# CELERYD_LOG_FORMAT = "[%(asctime)s: %(levelname)s/%(processName)s [%(task_name)s(%(task_id)s)] %(message)s"
CELERY_TASK_ACKS_LATE = False
CELERY_REJECT_ON_WORKER_LOST = True
# CELERYD_REDIRECT_STDOUTS_LEVEL = 'DEBUG'
CELERY_TRACK_STARTED = True
BROKER_TRANSPORT_OPTIONS = {
    'max_connections': 30,
    'health_check_interval': 20
}
CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {
    'visibility_timeout': 60 * 30,
    'health_check_interval': 20
}
# ------------------------------------------------CELERY END-----------------
{%- endif %}

REDIS_URL = os.getenv('REDIS_URL')

LOG_PATH = os.getenv("LOG_PATH")
LOG_LEVEL = os.getenv("LOG_LEVEL")
DATA_PATH = os.getenv("DATA_PATH")

fields.Field.default_error_messages["required"] = "必填项没值"
fields.Field.default_error_messages["null"] = "字段不可以为null"
fields.Field.default_error_messages["validator_failed"] = "值无效"
fields.Integer.default_error_messages = {"invalid": "不是一个有效的整数"}
validate.Length.message_min = "字段长度不允许小于最小长度 {min}"
validate.Length.message_max = "字段长度不允许超过最大长度{max}"
validate.Length.message_all = "字段长度必须大于 {min} 小于 {max}"
validate.Length.message_equal = "字段长度必须为 {equal}"
validate.Range.message_min = "必须 {min_op} {min}."
validate.Range.message_gte = "大于等于"