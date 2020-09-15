# -*- coding: utf-8 -*-
# @author: songjie
# @email: songjie@shanshu.ai
# @date: 2020/08/19
#      SJ编程规范
# 命名：
#    1. 见名思意，变量的名字必须准确反映它的含义和内容
#    2. 遵循当前语言的变量命名规则
#    3. 不要对不同使用目的的变量使用同一个变量名
#    4. 同个项目不要使用不同名称表述同个东西
#    5. 函数/方法 使用动词+名词组合，其它使用名词组合
# 设计原则：
#    1. KISS原则： Keep it simple and stupid !
#    2. SOLID原则： S: 单一职责 O: 开闭原则 L: 迪米特法则 I: 接口隔离原则 D: 依赖倒置原则
#
import os
import logging

from jinja2 import Environment, PackageLoader
from pick import pick

from {{cookiecutter.app_name}}.commons.db_util import dbtype_transfer
from {{cookiecutter.app_name}}.commons.utils.str_util import to_camel_case, to_pascal_case
from {{cookiecutter.app_name}}.extensions import db
from flask import current_app

from tests.generator.cust_filter import factoryboy_gen

logger = logging.getLogger(__name__)

model_path = os.path.join(os.path.dirname(__file__), "../..", '{{cookiecutter.app_name}}', "models")
resource_path = os.path.join(os.path.dirname(__file__), "../..", '{{cookiecutter.app_name}}', "api", 'resources')
schema_path = os.path.join(os.path.dirname(__file__), "../..", '{{cookiecutter.app_name}}', "api", 'schemas')
tmp_path = os.path.join(os.path.dirname(__file__), "../..", 'tmp', 'api')
tb_prefix = ''
jinjia_env = Environment(
    loader=PackageLoader('{{cookiecutter.app_name}}', 'templates'),
    autoescape=True)
jinjia_env.filters['to_camel_case'] = to_camel_case
jinjia_env.filters['to_pascal_case'] = to_pascal_case
jinjia_env.filters['dbtype_transfer'] = dbtype_transfer
jinjia_env.filters['factoryboy_gen'] = factoryboy_gen


def start():
    try:
        db_url = current_app.config.get('SQLALCHEMY_DATABASE_URI')
        db.reflect()
        choose_title1 = '请选择生成的代码模块:'
        choose_options1 = ['api', 'model']
        choose_selected1 = pick(choose_options1, choose_title1, multi_select=True, min_selection_count=1)
        choose_selected1 = list(map(lambda x: x[0], choose_selected1)) if choose_selected1 else None
        all_table = [{"tb_name": table_obj.name, "tb_obj": table_obj} for table_obj in db.get_tables_for_bind()]
        geterate_all_title = '请选择是否生成所有表:'
        geterate_all_options = [False, True]
        geterate_all_selected, geterate_all_idx = pick(geterate_all_options, geterate_all_title, multi_select=False, min_selection_count=1)
        if geterate_all_selected:
            geterate_tbs = all_table
        else:
            tb_title = '请选择要生成的数据表: '
            tb_options = all_table
            tb_selected_list_tuple = pick(tb_options, tb_title, multi_select=True, min_selection_count=1, options_map_func=lambda option: option.get('tb_name'))
            if tb_selected_list_tuple:
                geterate_tbs = list(map(lambda x: x[0], tb_selected_list_tuple))
            else:
                geterate_tbs = []
        for tb in geterate_tbs:
            var_dict = init_env_variable(tb.get('tb_name'), tb.get('tb_obj'))
            if 'model' in choose_selected1:
                generate_model(tb.get('tb_name'), tb.get('tb_obj'), db_url)
            if 'api' in choose_selected1:
                generate_resources(var_dict)

    except BaseException as e:
        logger.exception(e)


def generate_model(tb_name: str, tb_obj, db_url):
    logger.info("start generate %s", tb_name)
    if tb_prefix and tb_name.startswith(tb_prefix):
        tb_name = tb_name[len(tb_prefix):]
    outfile = os.path.abspath(os.path.join(model_path, tb_name.lower()))
    gen_cmd = f'flask-sqlacodegen  {db_url} --tables {tb_name} --outfile "{outfile}.py"  --flask'
    logger.info(gen_cmd)
    os.system(gen_cmd)
    logger.info("finish generate %s", tb_name)


def init_env_variable(tb_name: str, tb_obj):
    var_dict = dict()
    var_dict['tb_prefix'] = tb_prefix
    var_dict['tb_with_prefix_name'] = tb_name
    var_dict['tb_name'] = tb_name[len(tb_prefix):] if tb_prefix and tb_name.startswith(tb_prefix) else tb_name
    var_dict['tb_name'] = var_dict['tb_name'].lower()
    var_dict['title_lower'] = tb_name.lower()
    var_dict['tb_obj'] = tb_obj
    var_dict['columns'] = var_dict.get('tb_obj').columns
    var_dict['model_path'] = model_path
    var_dict['resource_path'] = resource_path
    var_dict['schema_path'] = schema_path
    var_dict['str_types'] = ['VARCHAR', 'CHAR', 'STRING']
    var_dict['datetime_types'] = ['TIMESTAMP', 'DATETIME']
    return var_dict


def generate_resources(var_dict: dict):
    resource_file_path = os.path.abspath(os.path.join(resource_path, f'{var_dict.get("tb_name")}.py'))
    schema_file_path = os.path.abspath(os.path.join(schema_path, f'{var_dict.get("tb_name")}.py'))
    apijson_file_path = os.path.abspath(os.path.join(tmp_path, f'{var_dict.get("tb_name")}.json'))
    assit_str_file_path = os.path.abspath(os.path.join(tmp_path, f'{var_dict.get("tb_name")}.txt'))
    # 1. 生成接口代码
    with open(resource_file_path, 'w') as resource_file:
        template = jinjia_env.get_template('resource.j2')
        resource_file.write(template.render(**var_dict))
    # 2. 生成schema 映射代码
    with open(schema_file_path, 'w') as schema_file:
        template = jinjia_env.get_template('schema.j2')
        schema_file.write(template.render(**var_dict))
    # 3. 生成 辅助信息帮助快速将生成的代码加入到项目中
    with open(assit_str_file_path, 'w') as assit_str_file:
        assit_template = jinjia_env.get_template('assit_str.j2')
        assit_str_file.write(assit_template.render(**var_dict))

    # 4. 生成api 返回的json 方便展示
    with open(apijson_file_path, 'w') as apijson_file:
        api_json_template = jinjia_env.get_template('api_json.j2')
        apijson_file.write(api_json_template.render(**var_dict))
