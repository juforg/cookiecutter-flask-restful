import logging

from flask import request, Blueprint
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import text

from {{cookiecutter.app_name}}.commons import db_util
from {{cookiecutter.app_name}}.commons.constants import return_code
from {{cookiecutter.app_name}}.models import Dict, DictItem
from {{cookiecutter.app_name}}.extensions import ma, db
from {{cookiecutter.app_name}}.commons.pagination import paginate
from marshmallow import fields
{%- if cookiecutter.use_excel == "yes" %}
import flask_excel as excel
{%- endif %}

logger = logging.getLogger(__name__)

dict_bp = Blueprint('dict', __name__, url_prefix='/api/v1')


class DictSchema(ma.Schema):
    id = fields.String(data_key='id')
    dict_name = fields.String(data_key='dictName')
    dict_code = fields.String(data_key='dictCode')
    description = fields.String(data_key='description')
    is_valid = fields.String(data_key='isValid')
    created_time = fields.String(dump_only=True, data_key='createdTime')
    updated_by = fields.String(dump_only=True, data_key='updatedBy')
    updated_time = fields.String(dump_only=True, data_key='updatedTime')


class DictDbSchema(ma.SQLAlchemySchema, DictSchema):
    class Meta:
        model = Dict
        sqla_session = db.session


class DictItemSchema(ma.Schema):
    id = fields.String(data_key='id')
    dict_code = fields.String(data_key='dictCode')
    item_code = fields.String(data_key='itemCode')
    item_name = fields.String(data_key='itemName')
    sort_order = fields.String(allow_none=True, data_key='sortOrder')
    description = fields.String(allow_none=True, data_key='description')
    is_valid = fields.String(data_key='isValid')
    created_time = fields.String(allow_none=True, data_key='createdTime')
    updated_by = fields.String(allow_none=True, dump_only=True, data_key='updatedBy')
    updated_time = fields.String(allow_none=True, dump_only=True, data_key='updatedTime')


class DictItemDbSchema(ma.SQLAlchemySchema, DictItemSchema):
    class Meta:
        model = DictItem
        sqla_session = db.session


class DictResource(Resource):
    """字典表 resource
    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: ymd
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
          name: ymd
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
          name: ymd
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
        schema = DictDbSchema()
        dict = Dict.query.get(id)
        if dict:
            return return_code.SUCCESS.data(schema.dump(dict.__dict__)).d, 200
        else:
            return return_code.NOT_FOUND.d, 200

    def put(self, id):
        session = db.session
        schema = DictDbSchema(unknown=True, partial=True)
        # dict = Dict.query.get(id)
        dict = schema.load(request.json)
        dict.updated_by = get_jwt_identity()
        session.merge(dict)
        session.commit()
        return return_code.SUCCESS.d, 200

    def delete(self, id):
        dict = Dict.query.get(id)
        if dict:
            db.session.delete(dict)
            db.session.commit()
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
        schema = DictDbSchema(many=True)
        dict_name = request.args.get("dictName")
        dict_code = request.args.get("dictCode")
        is_valid = request.args.get("isValid")
        sort = request.args.get("sort")
        query = Dict.query
        if dict_name:
            query = query.filter(Dict.dict_name.like('%'+dict_name+'%'))
        if dict_code:
            query = query.filter(Dict.dict_code.like('%'+dict_code+'%'))
        if is_valid:
            query = query.filter_by(is_valid=is_valid)
        if sort:
            query = query.order_by(text(sort))
        return return_code.SUCCESS.data(paginate(query, schema)), 200

    def post(self):
        session = db.session
        dictCode = request.json.get("dictCode")
        dict = session.query(Dict).filter_by(dict_code=dictCode).first()
        if dict:
            return return_code.ALREADY_EXIST, 200
        schema = DictDbSchema(unknown=True, partial=True)
        dict2 = schema.load(request.json)
        dict2.updated_by = get_jwt_identity()
        session.add(dict2)
        session.commit()
        return return_code.SUCCESS.d, 200

{%- if cookiecutter.use_excel == "yes" %}


@dict_bp.route('/dicts/export', methods=['POST'])
@jwt_required
def export_excel():
    query_sets = Dict.query.all()
    column_names = ['id', 'dict_name', 'dict_code', 'description', 'is_valid', 'created_time', 'updated_by',
                    'updated_time', ]
    colnames = ['主键', '字典名称', '字典编码', '描述', '是否有效', '创建时间', '更新人', '更新时间', ]
    return excel.make_response_from_query_sets(query_sets, column_names, file_type="xlsx",
                                               file_name='字典表', sheet_name='字典表', colnames=colnames)
{%- endif %}


@dict_bp.route('/dicts/list', methods=['POST'])
@jwt_required
def export_list():
    id = request.json.get('id', None)
    date_type = request.json.get('dateType', None)
    query = Dict.query. \
        with_entities(Dict.id, Dict.dict_name, Dict.dict_code, Dict.description, Dict.is_valid, Dict.created_time,
                      Dict.updated_by, Dict.updated_time, )
    if id:
        query = query.filter_by(id=id)
    if date_type:
        query = query.filter_by(date_type=date_type)
    schema = DictSchema(many=True)
    return return_code.SUCCESS.data(schema.dump(query.all())), 200

{%- if cookiecutter.use_excel == "yes" %}


@dict_bp.route('/dicts/import', methods=['POST'])
@jwt_required
def import_excel():
    session = db.session
    try:
        column_names = ['id', 'dict_name', 'dict_code', 'description', 'is_valid', 'created_time', 'updated_by',
                        'updated_time', ]
        records = request.get_records(field_name='file', name_columns_by_row=-1, start_row=1, auto_detect_int=False,
                                      colnames=column_names)
        db_util.increment_update(session=session,
                                 data_dict_list=records,
                                 schema_type=DictSchema,
                                 is_src=False,
                                 request_id=get_jwt_identity())
        session.commit()
    except BaseException as e:
        logger.exception(e)
        return return_code.UNKNOWN_ERROR.data(e.args)
    return return_code.SUCCESS.d, 200


{%- endif %}


class DictItemResource(Resource):
    method_decorators = [jwt_required]

    def get(self, id):
        schema = DictItemDbSchema()
        dict_item = DictItem.query.get(id)
        if dict_item:
            return return_code.SUCCESS.data(schema.dump(dict_item.__dict__)), 200
        else:
            return return_code.NOT_FOUND, 200

    def put(self, id):
        session = db.session
        schema = DictItemDbSchema(partial=True)
        # dict_item = DictItem.query.get(id)
        dict_item = schema.load(request.json)
        dict_item.updated_by = get_jwt_identity()
        session.merge(dict_item)
        session.commit()
        return return_code.SUCCESS.d, 200

    def delete(self, id):
        dict_item = DictItem.query.filter_by(id=id).first()
        if dict_item:
            db.session.delete(dict_item)
            db.session.commit()
        else:
            return return_code.NOT_FOUND.d, 200
        return return_code.SUCCESS.d, 200


class DictItemList(Resource):
    method_decorators = [jwt_required]

    def get(self, dict_code):
        schema = DictItemDbSchema(many=True)
        dict_item_query = DictItem.query.filter_by(dict_code=dict_code)
        is_valid = request.args.get("isValid")
        if is_valid:
            dict_item_query = dict_item_query.filter_by(is_valid=is_valid)
        query = dict_item_query.all()
        return return_code.SUCCESS.data(schema.dump(query)), 200

    def post(self, dict_code):
        session = db.session
        dict_items = request.json
        with session.begin(subtransactions=True):
            for item in dict_items:
                item['updatedBy'] = get_jwt_identity()
                item['dictDode'] = dict_code
                if item.get('id'):
                    session.query(DictItem).filter_by(id=item['id']).delete()
            schema = DictItemDbSchema(many=True, unknown=True)
            data = schema.load(dict_items)
            session.bulk_save_objects(data)
        session.commit()
        return return_code.SUCCESS, 200
