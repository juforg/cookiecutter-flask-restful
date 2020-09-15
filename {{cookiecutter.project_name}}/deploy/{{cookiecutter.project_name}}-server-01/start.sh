#!/bin/bash
PYTHON_PATH=/midware/python37/bin/
GUNICORN_BIN=$PYTHON_PATH/gunicorn
CELERY_BIN=$PYTHON_PATH/celery
APP_ROOT=/midware/app/{{cookiecutter.app_name}}
GUNICORN_PID=$APP_ROOT/workspace/{{cookiecutter.app_name}}/gunicorn.pid
CELERY_PID=$APP_ROOT/workspace/{{cookiecutter.app_name}}/celery-%n.pid
# CELERY 日志级别
CELERY_LOG_LEVEL=DEBUG
cd $APP_ROOT
echo "开始创建工作目录"
mkdir - p $APP_ROOT/workspace/{{cookiecutter.app_name}}/logs
mkdir - p $APP_ROOT/workspace/{{cookiecutter.app_name}}/data
echo "开始拷贝配置文件"
rm -f $APP_ROOT/.flaskenv
cp {{cookiecutter.app_name}}-dev.env .flaskenv

echo "开始安装依赖包"
exec $PYTHON_PATH/pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

echo "开始重启Flask Web"
if [ -f $GUNICORN_PID ]; then kill -HUP $(cat $GUNICORN_PID); fi
nohup $GUNICORN_BIN {{cookiecutter.app_name}}.wsgi:app \
      --workers=3 \
      --worker-class gevent \
      --pid $GUNICORN_PID \
      -t300 -b 0.0.0.0:5000 \
      > gunicorn-nohup.log 2>&1 &
echo "开始重启Celery"
nohup $CELERY_BIN multi restart worker -A {{cookiecutter.app_name}}.celery_app:app -E \
      --loglevel=$CELERY_LOG_LEVEL \
      --logfile=$APP_ROOT/workspace/{{cookiecutter.app_name}}/logs/celery-{{cookiecutter.app_name}}.log \
      --heartbeat-interval=15  \
      --concurrency=2 \
      --pidfile=$CELERY_PID \
      > celery-nohup.log 2>&1 &
echo "执行完成！"