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
from flask import request, Blueprint
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import text

from {{cookiecutter.app_name}}.commons import db_util
from {{cookiecutter.app_name}}.commons.constants import return_code
from {{cookiecutter.app_name}}.models.dict import Dict
from {{cookiecutter.app_name}}.api.schemas.dict import DictSchema
from {{cookiecutter.app_name}}.extensions import db
from {{cookiecutter.app_name}}.commons.pagination import paginate
{%- if cookiecutter.use_excel == "yes" %}
import flask_excel as excel {% endif%}

logger = logging.getLogger(__name__)

dict_bp = Blueprint('dict', __name__, url_prefix='/api/v1')


class DictResource(Resource):
    """字典 resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: id
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  dict: DictSchema
        404:
          description: dict does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: id
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              DictSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: dict updated
                  dict: DictSchema
        404:
          description: dict not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: id
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: dict deleted
        404:
          description: dict does not exists
    """
    method_decorators = [jwt_required]

    def get(self, id):
        schema = DictSchema(unknown=True,)
        dict = Dict.query.get(id)
        if dict:
            ret = schema.dump(dict.__dict__)
            return return_code.SUCCESS.set_data(ret).d, 200
        else:
            return return_code.NOT_FOUND.d, 200

    def put(self, id):
        session = db.session
        schema = DictSchema(unknown=True, partial=True)
        # dict = Dict.query.get(id)
        dict = schema.load(request.json)
        dict.updated_by = current_user.id
        session.merge(dict)
        session.flush()
        return return_code.SUCCESS.d, 200

    def post(self, id):
        schema = DictSchema(unknown=True)
        dict = schema.load(request.json)
        dict.updated_by = current_user.id
        db.session.add(dict)
        db.session.flush()

        return return_code.SUCCESS.d, 200

    def delete(self, id):
        dict = Dict.query.get(id)
        if dict:
            db.session.delete(dict)
            db.session.flush()
        else:
            return return_code.NOT_FOUND.d, 200

        return return_code.SUCCESS.d, 200


class DictList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/DictSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              DictSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: dict created
                  dict: DictSchema
    """
    method_decorators = [jwt_required]

    def get(self):
        schema = DictSchema(unknown=True, many=True)
        query = Dict.query. \
            with_entities(Dict.id, Dict.dict_name, Dict.dict_code, Dict.dict_desc, Dict.is_valid, Dict.org_code, Dict.create_by, Dict.create_time, Dict.update_by, Dict.update_time, Dict.revision, )
        req = request.args
        
        id = req.get('id')
        dict_name = req.get('dictName')
        dict_code = req.get('dictCode')
        dict_desc = req.get('dictDesc')
        is_valid = req.get('isValid')
        org_code = req.get('orgCode')
        create_by = req.get('createBy')
        create_time = req.get('createTime')
        update_by = req.get('updateBy')
        update_time = req.get('updateTime')
        revision = req.get('revision')
        
        if id:
            query = query.filter(Dict.id == id)
        if dict_name:
            query = query.filter(Dict.dict_name.like('%'+dict_name+'%'))
        if dict_code:
            query = query.filter(Dict.dict_code.like('%'+dict_code+'%'))
        if dict_desc:
            query = query.filter(Dict.dict_desc == dict_desc)
        if is_valid:
            query = query.filter(Dict.is_valid == is_valid)
        if org_code:
            query = query.filter(Dict.org_code == org_code)
        if create_by:
            query = query.filter(Dict.create_by == create_by)
        if create_time:
            query = query.filter(Dict.create_time == create_time)
        if update_by:
            query = query.filter(Dict.update_by == update_by)
        if update_time:
            query = query.filter(Dict.update_time == update_time)
        if revision:
            query = query.filter(Dict.revision == revision)
        data = paginate(query, schema)
        return return_code.SUCCESS.set_data(data).d, 200

    def post(self):
        schema = DictSchema(unknown=True, many=True)
        dicts = schema.load(request.json)
        for dict in dicts:
            dict.updated_by = current_user.id
        db.session.add_all(dicts)
        db.session.flush()

        return return_code.SUCCESS.d, 200


@dict_bp.route('/dicts/list', methods=['POST'])
@jwt_required
def query_list():
    schema = DictSchema(unknown=True, many=True)
    req = request.json
    
    id = req.get('id')
    dict_name = req.get('dictName')
    dict_code = req.get('dictCode')
    dict_desc = req.get('dictDesc')
    is_valid = req.get('isValid')
    org_code = req.get('orgCode')
    create_by = req.get('createBy')
    create_time = req.get('createTime')
    update_by = req.get('updateBy')
    update_time = req.get('updateTime')
    revision = req.get('revision')
    sort = req.get("sort", None)
    query = Dict.query. \
        with_entities(Dict.id, Dict.dict_name, Dict.dict_code, Dict.dict_desc, Dict.is_valid, Dict.org_code, Dict.create_by, Dict.create_time, Dict.update_by, Dict.update_time, Dict.revision, )
    
    if id:
        query = query.filter(Dict.id == id)
    if dict_name:
        query = query.filter(Dict.dict_name == dict_name)
    if dict_code:
        query = query.filter(Dict.dict_code == dict_code)
    if dict_desc:
        query = query.filter(Dict.dict_desc == dict_desc)
    if is_valid:
        query = query.filter(Dict.is_valid == is_valid)
    if org_code:
        query = query.filter(Dict.org_code == org_code)
    if create_by:
        query = query.filter(Dict.create_by == create_by)
    if create_time:
        query = query.filter(Dict.create_time == create_time)
    if update_by:
        query = query.filter(Dict.update_by == update_by)
    if update_time:
        query = query.filter(Dict.update_time == update_time)
    if revision:
        query = query.filter(Dict.revision == revision)
    if sort:
        query = query.order_by(text(sort))
    data = schema.dump(query.all())
    return return_code.SUCCESS.set_data(data).d, 200


{ % - if cookiecutter.use_excel == "yes" %}
@dict_bp.route('/dicts/export', methods=['POST'])
@jwt_required
def export_excel():
    query_sets = Dict.query.all()
    column_names = ['id', 'dict_name', 'dict_code', 'dict_desc', 'is_valid', 'org_code', 'create_by', 'create_time', 'update_by', 'update_time', 'revision', ]
    colnames = ['主键', '字典名称', '字典编码', '字典描述', '是否有效 Y启用 N不启用', '机构代码', '创建人', '创建时间', '更新人', '更新时间', '版本号', ]
    return excel.make_response_from_query_sets(query_sets, column_names, file_type="xlsx",
                                               file_name='字典', sheet_name='字典', colnames=colnames) {% endif%}


@dict_bp.route('/dicts/import', methods=['POST'])
@jwt_required
def import_excel():
    session = db.session
    try:
        column_names = ['id', 'dict_name', 'dict_code', 'dict_desc', 'is_valid', 'org_code', 'create_by', 'create_time', 'update_by', 'update_time', 'revision', ]
        records = request.get_records(field_name='file', name_columns_by_row=-1, start_row=1, auto_detect_int=False, colnames=column_names)
        db_util.increment_update(session=session,
                                 data_dict_list=records,
                                 schema_type=DictSchema,
                                 is_src=False,
                                 request_id=current_user.id)
        session.flush()
    except BaseException as e:
        logger.exception(e)
        return return_code.UNKNOWN_ERROR.set_data(e.args).d
    return return_code.SUCCESS.d, 200