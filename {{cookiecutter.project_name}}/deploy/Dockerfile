# This is a simple Dockerfile to use while developing
# It's not suitable for production
#
# It allows you to run both flask and celery if you enabled it
# for flask: docker run --env-file=.flaskenv image flask run
# for celery: docker run --env-file=.flaskenv image celery worker -A myapi.celery_app:app
#
# note that celery will require a running broker and result backend
FROM {{cookiecutter.app_name}}-base
ARG USER_ID
RUN echo $USER_ID
RUN ln -sf /usr/share/zoneinfo/Asia/ShangHai /etc/localtime
RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN groupadd -g $USER_ID -r app && useradd -u $USER_ID -r -g app app
RUN mkdir -p /opt/{{cookiecutter.app_name}}/code \
    && mkdir -p /opt/{{cookiecutter.app_name}}/logs \
    && mkdir -p /opt/{{cookiecutter.app_name}}/data

WORKDIR /opt/{{cookiecutter.app_name}}/code

ADD {{cookiecutter.app_name}}-be.tar.gz /opt/{{cookiecutter.app_name}}/code/
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple \
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
    && pip install -e .\
    && pip install gunicorn -i https://mirrors.aliyun.com/pypi/simple

RUN pip install -e .

RUN chown -R app:app /opt/*

USER app