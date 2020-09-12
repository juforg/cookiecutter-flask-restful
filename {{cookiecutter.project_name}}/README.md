## 项目简介
1. XXX


## 技术选型
1. Python3.7
2. python web框架 --> Flask
3. restful框架 <https://flask-restful.readthedocs.io/en/latest>
4. swagger 框架 <https://github.com/rantav/flask-restful-swagger>
6. 本项目脚手架<https://github.com/karec/cookiecutter-flask-restful>
7. 数据库连接 pymysql
8. 接口文档 <https://github.com/marshmallow-code/apispec>

## 环境准备
```bash
brew install pyenv
brew install pyenv-virtualenv
pyenv init
```
按照提示 把 `eval "$(pyenv init -)"` 
放入到zshrc这个文件最后一行
```
vi ~/.zshrc
source ~/.zshrc
```
#### python版本
- 显示可安装python版本
    `pyenv install -l`
- 安装指定Python版本
    `pyenv install 3.7.2`
- 卸载指定python版本
    `pyenv uninstall 3.7.2`
- 显示已安装python版本 包括虚拟环境
    `pyenv versions`
- 设置当前目录python版本
    `pyenv local 3.7.2`
- 设置当前会话python版本
    `pyenv shell 3.7.2`
- 重置版本设置
    ```bash
    pyenv shell --unset
    pyenv local --unset
    ```
#### 虚拟环境

- 创建某个Python版本的虚拟环境
    `pyenv virtualenv 3.7.2 {{cookiecutter.app_name}}-venv`
- 激活和停用虚拟环境：
    `pyenv activate {{cookiecutter.app_name}}-venv`
    `pyenv deactivate`
- 列出当前所有的虚拟环境：
    `pyenv virtualenvs`
- 删除虚拟环境：
    `pyenv virtualenv-delete {{cookiecutter.app_name}}-venv`
## 安装依赖:
1. `pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/`

|包名|说明|版本要求|
|----|----|----|
|python-dotenv|加载.flaskenv配置到环境变量中||
|mip|混合整数规划|1.9.0|
|PuLP|混合整数规划|2.0|
|celery|异步任务/定时任务框架|4.3|
|flask-redis|redis集成|可被当作分布式锁|
|Flask-Excel|excel集成|导入导出及操作excel|
|marshmallow|序列化反序列化包|3|
|pandas|结构化数据的分析工具集||
|sqlacodegen|生成sqlalchemy的model代码||
|cachetools|方法结果缓存||
|pyarmor|python代码加密||
|aiohttp|异步http请求||
|pick|命令行选则器||
|click|flask命令行强化|7.0|
|joblib|模型转文件||

## 本地启动:
- pycharm 启动
![](http://wntc.oss-cn-shanghai.aliyuncs.com/2019/8/9/1565328268382.png)
- 启动异步任务
![](http://wntc.oss-cn-shanghai.aliyuncs.com/2019/8/29/1567073039461.png)
`worker -A {{cookiecutter.app_name}}.celery_app:app --loglevel=info -B -E -Q CELERY_ASYNC_QUEUE_ABINBEV_ZIY_FAC_OUT,CELERY_ASYNC_QUEUE_ABINBEV_ZIY_FAC_IN,CELERY_ASYNC_QUEUE_ABINBEV_ZIY_FAC_OTHER --logfile=/opt/{{cookiecutter.app_name}}/logs/celery-{{cookiecutter.app_name}}.log`
- 启动定时任务
![](http://wntc.oss-cn-shanghai.aliyuncs.com/2019/10/17/1571296058664.png)
`worker -A {{cookiecutter.app_name}}.celery_app:app --loglevel=info -Q timing_tasks_q -E -c 2`
- 命令行启动
    - `pip install -e .`
    - `{{cookiecutter.app_name}} init`
    - `{{cookiecutter.app_name}} run`

- 生成代码
![](http://wntc.oss-cn-shanghai.aliyuncs.com/2019/10/19/1571492916689.png)
![generate_model](https://i.loli.net/2020/08/23/tcF34CwQox96Vkz.png)

- 启动flower监控celery
![](https://i.loli.net/2019/12/18/GfBqLFyVhlPeco4.png)

- 同步数据到本地
![](http://wntc.oss-cn-shanghai.aliyuncs.com/2020/1/13/1578903041167.png)

## 接口文档
http://localhost:5000/swagger-ui

## 目录结构
````
├── README.md
├── {{cookiecutter.app_name}}                   应用目录
│   ├── __init__.py
│   ├── api              对外开放接口
│   │   ├── __init__.py
│   │   └── views.py
|   ├── algo             算法核心程序
|   ├── auth             登录专用接口目录
|   ├── commons          可复用代码目录
│   │   └── constants    常量定义目录
│   │   │   └── const.py    常量定义
│   │   │   └── return_code.py    错误码定义
│   │   └── utils        工具类
│   ├── extensions.py   第三方组件初始化
│   └── models          数据模型目录
│   └── tasks           celery异步定时任务目录
├── config.py           配置相关
├── dist                生成加密文件目录 用于发布
├── requirements.txt    主程序必备pip包列表
├── test_requirements.txt    测试用pip包非必须
├── freeze_requirements.txt    稳定的pip包,注意不能安装垃圾
└── tests               测试问目录
└── sql                 存放数据库脚本目录
````

## 配置
- 环境变量
安装`python-dotenv` 包后 会自动加载 `.env` 和`.flaskenv`文件，.env 文件会覆盖.flaskenv的配置，适合本地特殊配置，但不能够提交


## 部署
1. 修改poc服务器上环境变量文件 
2. 运行deploy.py

## 算法源码加密
https://github.com/dashingsoft/pyarmor

## 编码实践
1. 打印日志
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("debug")
logger.info("%s init rabbitmq start",'requestId')
logger.warn("warn")
logger.error("error")
logger.exception(e) #打印异常堆栈

```

2. 添加新的接口类
在api目录下新建类，在api/__init__.py文件中添加文件名，在app.py中 register_blueprints 方法里添加相应的类
![](http://wntc.oss-cn-shanghai.aliyuncs.com/2019/8/27/1566885631639.png)
![](http://wntc.oss-cn-shanghai.aliyuncs.com/2019/8/27/1566885639495.png)
![](http://wntc.oss-cn-shanghai.aliyuncs.com/2019/8/27/1566885651762.png)

3. swagger接口文档
  - 定义接口及路径
    ![](http://wntc.oss-cn-shanghai.aliyuncs.com/2019/8/27/1566885715631.png)
  - 注册该接口
    ![](http://wntc.oss-cn-shanghai.aliyuncs.com/2019/8/27/1566885779389.png)

4. sqlacchemy
    - 自定义表名 `__tablename__ = 'order'`
    - 指定model数据源 `__bind_key__ = 'flux_{{cookiecutter.app_name}}'`
    - 有则更新无则修改`session.merge(model)`
    - 保存对象列表`db.session.add_all(tasks)`
    
## 设置mysql 事务隔离级别
```
SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
set session transaction isolation level read committed; 
select @@global.tx_isolation,@@tx_isolation;
```

[python编码规范](https://internal.cardopt.com/confluence/pages/viewpage.action?pageId=6979785)
5. pandas的DataFrame 数去数据库,利用sqlalchemy选择数据源
    - 默认数据源
    `pd.read_sql(query.statement, query.session.bind,columns=const.MATERIAL_COLUMNS_NAMES)`
    - 指定数据源
    `pd.read_sql(invs_query.statement, db.get_engine(bind=const.DATA_SOURCE_FLUX_WMS),columns=const.INV_COLUMNS_NAMES)`
    
 ## 日志滚动
 使用 linux 自带的 logrotate
 https://blog.zengrong.net/post/flask-uwsgi-logging-rotate/
{%- if cookiecutter.use_oracle == "yes" %}
`cp instantclient-basic-macos.x64-11.2.0.4.0.zip /opt/oracle/`
`cp /opt/oracle/instantclient_11_2/{libclntsh.dylib.11.1,libnnz11.dylib,libociei.dylib} ~/lib/`
![](http://wntc.oss-cn-shanghai.aliyuncs.com/2019/11/16/1573912336527.png)

https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
https://www.oracle.com/database/technologies/instant-client/macos-intel-x86-downloads.html 
{%- endif %}



## 文档
- http://www.pythondoc.com/flask/index.html
- http://www.pythondoc.com/flask-sqlalchemy/index.html
- http://www.pythondoc.com/Flask-RESTful/
- https://www.osgeo.cn/sqlalchemy/core/tutorial.html#selecting
- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql.html#pandas.read_sql
- http://www.pythondoc.com/
- https://www.v2ex.com/t/383174?p=1
- http://docs.celeryproject.org/en/latest/userguide/configuration.html#logging
- https://marshmallow.readthedocs.io/en/stable/api_reference.html#module-marshmallow.fields
- https://blog.csdn.net/qq_18598403/article/details/93382513
- https://www.jianshu.com/p/769b907836a6
- https://www.jianshu.com/p/0946da4ccd40
- https://unpluggedcoder.me/2018/05/03/Asynchronous-logging-with-Python/index.html
- https://github.com/SPSCommerce/redlock-py
- https://linux.cn/article-4126-1.html
- https://github.com/TheWaWaR/flask-redlock
- https://flower.readthedocs.io/
- https://www.cnblogs.com/xybaby/p/9197032.html
- https://medium.com/@rob.blackbourn/how-to-use-python-logging-queuehandler-with-dictconfig-1e8b1284e27a
- https://www.cnblogs.com/cwp-bg/p/8759638.html