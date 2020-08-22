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
from pick import pick
from {{cookiecutter.app_name}}.extensions import db
from flask import current_app
logger = logging.getLogger(__name__)


model_path = os.path.join(os.getcwd(), "../", '{{cookiecutter.app_name}}', "models")
tb_prefix = ''


def start():
    try:
        db_url = current_app.config.get('SQLALCHEMY_DATABASE_URI')
        db.reflect()
        all_table = [{"tb_name": table_obj.name, "tb_obj": table_obj} for table_obj in db.get_tables_for_bind()]
        geterate_all_title = '请选择是否生成所有表:'
        geterate_all_options = [False, True]
        geterate_all_selected, geterate_all_idx = pick(geterate_all_options, geterate_all_title, multi_select=False, min_selection_count=1)
        if geterate_all_selected:
            geterate_tbs = all_table
        else:
            tb_title = '请选择要生成的数据表: '
            tb_options = all_table
            tb_selected_list_tuple = pick(tb_options, tb_title, multi_select=True, options_map_func=lambda option: option.get('tb_name'))
            if tb_selected_list_tuple:
                geterate_tbs = list(map(lambda x: x[0], tb_selected_list_tuple))
            else:
                geterate_tbs = []
        for tb in geterate_tbs:
            geterate_table(tb.get('tb_name'), tb.get('tb_obj'), db_url)

    except BaseException as e:
        logger.exception(e)


def geterate_table(tb_name: str, tb_obj, db_url):
    logger.info("start generate %s", tb_name)
    if tb_prefix and tb_name.startswith(tb_prefix):
        tb_name = tb_name[len(tb_prefix):]
    outfile = os.path.abspath(os.path.join(model_path, tb_name))
    gen_cmd = f'flask-sqlacodegen  {db_url} --tables {tb_name} --outfile "{outfile}.py"  --flask'
    logger.info(gen_cmd)
    os.system(gen_cmd)
    logger.info("finish generate %s", tb_name)

# if __name__ == '__main__':
#     start()
