FROM python:3.7.2-slim-stretch
{%- if cookiecutter.use_LightGBM == "yes" %}
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    cmake \
    build-essential \
    gcc \
    g++ \
    git \
    gnupg2 \
    curl \
    apt-transport-https \
    wget && \
    {%- if cookiecutter.use_mssql == "yes" %}
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools \
#    freetds-dev \
    unixodbc-dev && \
    {%- endif %}
    git clone --recursive --branch v2.2.3 --depth 1 https://github.com/Microsoft/LightGBM && \
#    git checkout v2.2.3 && \
    cd LightGBM/python-package && python setup.py install && \
    # clean
    apt-get autoremove -y && apt-get clean && \
    rm -rf /usr/local/src/*
{%- endif %}


ADD requirements.txt /requirements.txt
RUN pip install pystan -i https://mirrors.aliyun.com/pypi/simple
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
    && pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple

#ENTRYPOINT /bin/bash
