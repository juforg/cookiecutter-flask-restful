# -*- coding: utf-8 -*-
# @author: songjie
# @email: songjie@shanshu.ai
# @date: 2020/09/02
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

import logging
import os
from flask import current_app, make_response
from flask import request, Blueprint, send_from_directory
from flask_jwt_extended import jwt_required
from {{cookiecutter.app_name}}.commons.constants import return_code

logger = logging.getLogger(__name__)

download_bp = Blueprint('download', __name__, url_prefix='/api/v1')


@download_bp.route('/download_template', methods=['GET'])
@jwt_required
def download_template():
    """

    :return:
    """
    file_name = request.args.get('fileName', None)
    if file_name:
        file_path = os.path.abspath(os.path.join(os.getenv("DATA_PATH", "/var/algo/data/"), 'template'))
        if os.path.isfile(os.path.join(file_path, file_name)):
            # response = make_response(send_from_directory(file_path, file_name, as_attachment=True))
            # response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))
            return send_from_directory(file_path, file_name, as_attachment=True)
    return return_code.FILE_NOT_FOUND.d, 200
