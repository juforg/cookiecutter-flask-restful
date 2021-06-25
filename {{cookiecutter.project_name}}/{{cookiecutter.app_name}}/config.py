"""Default configuration

Use env var to override
"""
import os, datetime
from marshmallow import fields, validate
from sqlalchemy.pool import QueuePool

ENV = os.getenv("FLASK_ENV")
# DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_BINDS = {
#     'transfer_db': os.getenv("SQLALCHEMY_BINDS_TRANSFER")
# }
# 如果设置为Ture， SQLAlchemy 会记录所有 发给 stderr 的语句，这对调试有用。(打印sql语句)#sql 日志
SQLALCHEMY_ECHO = True if os.getenv("SQLALCHEMY_ECHO") == "True" else False
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': int(os.getenv("SQLALCHEMY_POOL_SIZE", "0")),
    'max_overflow': int(os.getenv("SQLALCHEMY_POOL_OVERFLOW", "2")),
    # 如果为True，则连接池将记录信息输出，例如连接失效时以及连接被回收到默认日志处理程序时，默认sys.stdout为输出。如果设置为字符串 "debug"，则日志记录将包括池检出和签入。使用标准Python logging模块也可以直接控制日志记录
    'echo_pool': 'debug' if os.getenv("SQLALCHEMY_ECHO_POOL") == "True" else False,
    # 默认2小时。该值一定要比数据库wait_timeout小，否则它不起作用
    'pool_recycle': 60 * 60,
    'pool_timeout': int(os.getenv("SQLALCHEMY_POOL_TIMEOUT", "20")),
    'pool_pre_ping': True,   # 测试是否可用
    'pool_use_lifo': False,   # 越老的越容易被回收，一定要跟ping 配合，否则老的极易被回收造成连接不可用
    'poolclass': QueuePool,  # flask 应用可以设QueuePool，celery应用可能不用池
    'isolation_level': 'AUTOCOMMIT',
    'connect_args': {
                    'ssl': {'ca': None}, #开启ssl连接的数据库配置
                     # "init_command": "SET SESSION time_zone='+08:00'" # 设置时区防止数据库时区不对
                     }
}

# ------------------------------------------------JWT START-----------------
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
ROPAGATE_EXCEPTIONS = True # 异常向父任务传送
CELERY = {
    "broker_url": os.getenv("CELERY_BROKER_URL"),
    "result_backend": os.getenv("CELERY_RESULT_BACKEND_URL"),
    "task_default_queue": os.getenv("CELERY_TASK_DEFAULT_QUEUE", "{{cookiecutter.app_name}}:celery"), # 修改默认队列名，防止不同应用使用同个broker出现问题
    "timezone": 'Asia/Shanghai',
    # "enable_utc": True,
    "task_ignore_result": True,  # 任务结果不缓存
    "task_serializer": 'json',  # 任务序列化和反序列化使用方案 Can be json (default), pickle, yaml, msgpack
    "result_serializer": 'json',  # 读取任务结果一般性能要求不高，所以使用可读性更好的json
    "accept_content": ['json'], # 指定接收的内容类型 可选 , 'msgpack', 'pickle'
    # "worker_concurrency": 1 , # 并发只有一个进程消费
    # "worker_prefetch_multiplier": 1 , # 每次获取几个任务
    # "worker_max_memory_per_child": int(celery_max_mem_kilobytes / app.conf.worker_concurrency) , # 最大内存,单个任务超过限制，完成后会新建
    "worker_max_tasks_per_child": 10,        # 每个worker最多执行万10个任务就会被销毁，可防止内存泄露
    "result_expires": 60 * 10,  # 任务结果过期时间
    "task_time_limit": 60 * 60 * 2 , # 任务超时时间
    "worker_hijack_root_logger": True,  # ：默认true，先前所有的logger的配置都会失效，可以通过设置false禁用定制自己的日志处理程序；
    "worker_task_log_format": "%(asctime)s %(levelname)s <PID %(process)d:%(processName)s> %(name)s.%(funcName)s(): %(message)s",
    "worker_log_format": "%(asctime)s %(levelname)s <PID %(process)d:%(processName)s> %(name)s.%(funcName)s(): %(message)s",
    # "task_acks_late": False,  # 可能会导致任务跑多次
    # "task_reject_on_worker_lost": False,  # 可能会导致任务跑多次
    # "worker_redirect_stdouts_level": 'DEBUG',
    "task_track_started": True,  # 是任务有开始状态
    'event_queue_prefix': '{{cookiecutter.app_name}}:celeryev',
    "broker_transport_options": {
        'max_connections': 30,
        'health_check_interval': 20,
        'queue_name_prefix': '{{cookiecutter.app_name}}:', # only for SQS  & AZURE SERVICE
        'unacked_mutex_key': '{{cookiecutter.app_name}}:unacked_mutex',
        'unacked_index_key': '{{cookiecutter.app_name}}:unacked_index',
        'unacked_key': '{{cookiecutter.app_name}}:unacked',
    },
    "result_backend_transport_options": {
        'visibility_timeout': 60 * 30,
        'health_check_interval': 20
    }
}
CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁
# C_FORCE_ROOT = 'true'  # 允许root用户启动celery

# ------------------------------------------------CELERY END-----------------
{%- endif %}

REDIS_URL = os.getenv('REDIS_URL')

LOG_PATH = os.getenv("LOG_PATH")
LOG_LEVEL = os.getenv("LOG_LEVEL")
DATA_PATH = os.getenv("DATA_PATH")