FLASK_ENV=development
FLASK_APP={{cookiecutter.app_name}}.app:create_app
FLASK_RUN_PORT=5000
SECRET_KEY={{cookiecutter.app_name}}
JWT_COOKIE_CSRF_PROTECT=False
DATABASE_URI=sqlite:////tmp/{{cookiecutter.app_name}}.db
{%- if cookiecutter.use_mssql == "yes" %}
SQLALCHEMY_BINDS_XXX1=mssql+pyodbc://SA:Shanshu.ai@10.10.0.138:1434/WHAI?driver=ODBC+Driver+17+for+SQL+Server
{%- endif %}
{%- if cookiecutter.use_oracle == "yes" %}
SQLALCHEMY_BINDS_XXX2=oracle+cx_oracle://SPCS_WMS:123456@10.10.0.138:1522/helowin
NLS_LANG=AMERICAN_AMERICA.AL32UTF8
{%- endif %}
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/
LOG_PATH=./all.log
DATA_PATH=.