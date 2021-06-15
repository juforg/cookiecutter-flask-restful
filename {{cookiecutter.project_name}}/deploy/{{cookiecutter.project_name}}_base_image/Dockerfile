FROM python:3.7.4-slim-stretch
{%- if cookiecutter.use_oracle == "yes" %}
ENV LD_LIBRARY_PATH="/usr/local/lib;/usr/local/instantclient"
ENV NLS_LANG="AMERICAN_AMERICA.AL32UTF8"
{%- endif %}

RUN echo " " > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ stretch main non-free contrib" >> /etc/apt/sources.list &&\
    echo "deb http://mirrors.aliyun.com/debian-security stretch/updates main" >> /etc/apt/sources.list &&\
    echo "deb http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib" >> /etc/apt/sources.list &&\
    echo "deb http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" >> /etc/apt/sources.list

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
    {%- if cookiecutter.use_oracle == "yes" %}
    libaio1 \
    unzip \
    {%- endif %}
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
    #oracle
    wget https://github.com/pwnlabs/oracle-instantclient/raw/master/instantclient-basic-linux.x64-11.2.0.4.0.zip -O /tmp/instantclient-basic-linux.x64-11.2.0.4.0.zip && \
    unzip /tmp/instantclient-basic-linux.x64-11.2.0.4.0.zip -d /usr/local/ && \
    ln -s /usr/local/instantclient_11_2 /usr/local/instantclient && \
    ln -s /usr/local/instantclient/libclntsh.so.11.1 /usr/local/instantclient/libclntsh.so
    # clean
    apt-get autoremove -y && apt-get clean && \
    rm -rf /usr/local/src/*
{%- endif %}


ADD requirements.txt /requirements.txt
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple \
    {%- if cookiecutter.use_LightGBM == "yes" %}
    && pip install pystan -i https://mirrors.aliyun.com/pypi/simple \
    {%- endif %}
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# clean
RUN apt-get clean -y && \
    apt-get autoclean -y && \
    apt-get remove -y  g++ && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /var/lib/log/* /tmp/* /var/tmp/*

#ENTRYPOINT /bin/bash
