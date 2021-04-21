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
from {{cookiecutter.app_name}}.models.dict_item import DictItem
from {{cookiecutter.app_name}}.api.schemas.dict_item import DictItemSchema
from {{cookiecutter.app_name}}.extensions import db
from {{cookiecutter.app_name}}.commons.pagination import paginate
import flask_excel as excel

logger = logging.getLogger(__name__)

dict_item_bp = Blueprint('dict_item', __name__, url_prefix='/api/v1')


class DictItemResource(Resource):
    """字典明细 resource

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
                  dict_item: DictItemSchema
        404:
          description: dict_item does not exists
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
              DictItemSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: dict_item updated
                  dict_item: DictItemSchema
        404:
          description: dict_item not exists
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
                    example: dict_item deleted
        404:
          description: dict_item does not exists
    """
    method_decorators = [jwt_required]

    def get(self, id):
        schema = DictItemSchema(unknown=True,)
        dict_item = DictItem.query.get(id)
        if dict_item:
            ret = schema.dump(dict_item.__dict__)
            return return_code.SUCCESS.set_data(ret).d, 200
        else:
            return return_code.NOT_FOUND.d, 200

    def put(self, id):
        session = db.session
        schema = DictItemSchema(unknown=True, partial=True)
        # dict_item = DictItem.query.get(id)
        dict_item = schema.load(request.json)
        dict_item.updated_by = current_user.id
        session.merge(dict_item)
        session.flush()
        return return_code.SUCCESS.d, 200

    def post(self, id):
        schema = DictItemSchema(unknown=True)
        dict_item = schema.load(request.json)
        dict_item.updated_by = current_user.id
        db.session.add(dict_item)
        db.session.flush()

        return return_code.SUCCESS.d, 200

    def delete(self, id):
        dict_item = DictItem.query.get(id)
        if dict_item:
            db.session.delete(dict_item)
            db.session.flush()
        else:
            return return_code.NOT_FOUND.d, 200

        return return_code.SUCCESS.d, 200


class DictItemList(Resource):
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
                          $ref: '#/components/schemas/DictItemSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              DictItemSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: dict_item created
                  dict_item: DictItemSchema
    """
    method_decorators = [jwt_required]

    def get(self):
        schema = DictItemSchema(unknown=True, many=True)
        query = DictItem.query. \
            with_entities(DictItem.id, DictItem.dict_code, DictItem.item_code, DictItem.item_value, DictItem.sort_no, DictItem.item_desc, DictItem.is_valid, DictItem.org_code, DictItem.create_by, DictItem.create_time, DictItem.update_by, DictItem.update_time, DictItem.revision, )
        req = request.args
        
        id = req.get('id')
        dict_code = req.get('dictCode')
        item_code = req.get('itemCode')
        item_value = req.get('itemValue')
        sort_no = req.get('sortNo')
        item_desc = req.get('itemDesc')
        is_valid = req.get('isValid')
        org_code = req.get('orgCode')
        create_by = req.get('createBy')
        create_time = req.get('createTime')
        update_by = req.get('updateBy')
        update_time = req.get('updateTime')
        revision = req.get('revision')
        
        if id:
            query = query.filter(DictItem.id == id)
        if dict_code:
            query = query.filter(DictItem.dict_code == dict_code)
        if item_code:
            query = query.filter(DictItem.item_code == item_code)
        if item_value:
            query = query.filter(DictItem.item_value == item_value)
        if sort_no:
            query = query.filter(DictItem.sort_no == sort_no)
        if item_desc:
            query = query.filter(DictItem.item_desc == item_desc)
        if is_valid:
            query = query.filter(DictItem.is_valid == is_valid)
        if org_code:
            query = query.filter(DictItem.org_code == org_code)
        if create_by:
            query = query.filter(DictItem.create_by == create_by)
        if create_time:
            query = query.filter(DictItem.create_time == create_time)
        if update_by:
            query = query.filter(DictItem.update_by == update_by)
        if update_time:
            query = query.filter(DictItem.update_time == update_time)
        if revision:
            query = query.filter(DictItem.revision == revision)
        data = paginate(query, schema)
        return return_code.SUCCESS.set_data(data).d, 200

    def post(self):
        schema = DictItemSchema(unknown=True, many=True)
        dict_items = schema.load(request.json)
        for dict_item in dict_items:
            dict_item.updated_by = current_user.id
            dict_item.org_code = current_user.org_code
        db.session.add_all(dict_items)
        db.session.flush()

        return return_code.SUCCESS.d, 200


@dict_item_bp.route('/dict_items/list', methods=['POST'])
@jwt_required
def query_list():
    schema = DictItemSchema(unknown=True, many=True)
    req = request.json
    
    id = req.get('id')
    dict_code = req.get('dictCode')
    item_code = req.get('itemCode')
    item_value = req.get('itemValue')
    sort_no = req.get('sortNo')
    item_desc = req.get('itemDesc')
    is_valid = req.get('isValid')
    org_code = req.get('orgCode')
    create_by = req.get('createBy')
    create_time = req.get('createTime')
    update_by = req.get('updateBy')
    update_time = req.get('updateTime')
    revision = req.get('revision')
    sort = req.get("sort", None)
    query = DictItem.query. \
        with_entities(DictItem.id, DictItem.dict_code, DictItem.item_code, DictItem.item_value, DictItem.sort_no, DictItem.item_desc, DictItem.is_valid, DictItem.org_code, DictItem.create_by, DictItem.create_time, DictItem.update_by, DictItem.update_time, DictItem.revision, )
    
    if id:
        query = query.filter(DictItem.id == id)
    if dict_code:
        query = query.filter(DictItem.dict_code == dict_code)
    if item_code:
        query = query.filter(DictItem.item_code == item_code)
    if item_value:
        query = query.filter(DictItem.item_value == item_value)
    if sort_no:
        query = query.filter(DictItem.sort_no == sort_no)
    if item_desc:
        query = query.filter(DictItem.item_desc == item_desc)
    if is_valid:
        query = query.filter(DictItem.is_valid == is_valid)
    if org_code:
        query = query.filter(DictItem.org_code == org_code)
    if create_by:
        query = query.filter(DictItem.create_by == create_by)
    if create_time:
        query = query.filter(DictItem.create_time == create_time)
    if update_by:
        query = query.filter(DictItem.update_by == update_by)
    if update_time:
        query = query.filter(DictItem.update_time == update_time)
    if revision:
        query = query.filter(DictItem.revision == revision)
    if sort:
        query = query.order_by(text(sort))
    data = schema.dump(query.all())
    return return_code.SUCCESS.set_data(data).d, 200


@dict_item_bp.route('/dict_items/export', methods=['POST'])
@jwt_required
def export_excel():
    query_sets = DictItem.query.all()
    column_names = ['id', 'dict_code', 'item_code', 'item_value', 'sort_no', 'item_desc', 'is_valid', 'org_code', 'create_by', 'create_time', 'update_by', 'update_time', 'revision', ]
    colnames = ['主键', '字典编码', '项编码', '项值', '排序', '描述', '是否有效 Y启用 N不启用', '机构代码', '创建人', '创建时间', '更新人', '更新时间', '版本号', ]
    return excel.make_response_from_query_sets(query_sets, column_names, file_type="xlsx",
                                               file_name='字典明细', sheet_name='字典明细', colnames=colnames)


@dict_item_bp.route('/dict_items/import', methods=['POST'])
@jwt_required
def import_excel():
    session = db.session
    try:
        column_names = ['id', 'dict_code', 'item_code', 'item_value', 'sort_no', 'item_desc', 'is_valid', 'org_code', 'create_by', 'create_time', 'update_by', 'update_time', 'revision', ]
        records = request.get_records(field_name='file', name_columns_by_row=-1, start_row=1, auto_detect_int=False, colnames=column_names)
        db_util.increment_update(session=session,
                                 data_dict_list=records,
                                 schema_type=DictItemSchema,
                                 is_src=False,
                                 request_id=current_user.id)
        session.flush()
    except BaseException as e:
        logger.exception(e)
        return return_code.UNKNOWN_ERROR.set_data(e.args).d
    return return_code.SUCCESS.d, 200