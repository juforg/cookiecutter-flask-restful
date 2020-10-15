#!/bin/bash
PYTHON_PATH=/midware/python37/bin
GUNICORN_BIN=$PYTHON_PATH/gunicorn
CELERY_BIN=$PYTHON_PATH/celery
APP_ROOT=/midware/app
WORK_SPACE=/midware/workspace
GUNICORN_PID=$WORK_SPACE/{{cookiecutter.app_name}}/gunicorn.pid
CELERY_PID=$WORK_SPACE/{{cookiecutter.app_name}}/celery-%n.pid
# CELERY 日志级别
CELERY_LOG_LEVEL=DEBUG
cd $APP_ROOT
echo "开始创建工作目录"
mkdir -p $WORK_SPACE/{{cookiecutter.app_name}}/logs
mkdir -p $WORK_SPACE/{{cookiecutter.app_name}}/data
echo "开始重命名配置文件"
rm -f .flaskenv
cp {{cookiecutter.app_name}}-dev.env .flaskenv
echo "创建日志文件"
echo "准备重启。。。" >> $WORK_SPACE/{{cookiecutter.app_name}}/logs/{{cookiecutter.app_name}}.log
echo "准备重启。。。" >> $WORK_SPACE/{{cookiecutter.app_name}}/logs/celery-{{cookiecutter.app_name}}.log
chmod 777 -R $WORK_SPACE

echo "开始安装依赖包"
echo "$PYTHON_PATH/pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com"
$PYTHON_PATH/pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

echo "开始重启"
if [ ! -f /tmp/supervisord.pid ]; then
  echo "启动supervisord守护进程"
  $PYTHON_PATH/supervisord -c $APP_ROOT/supervisord.conf -u sulipadmin@jqdev
  $PYTHON_PATH/supervisorctl -c $APP_ROOT/supervisord.conf -u sulipadmin@jqdev
fi
$PYTHON_PATH/supervisorctl reload
echo "执行完成！"