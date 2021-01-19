from flask import request, Blueprint
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_current_user, get_jwt_identity
from {{cookiecutter.app_name}}.commons import db_util, common_fun
from {{cookiecutter.app_name}}.api.schemas.user import UserSchema
from {{cookiecutter.app_name}}.commons.constants import const
from {{cookiecutter.app_name}}.commons.constants import return_code
from {{cookiecutter.app_name}}.models import User
from {{cookiecutter.app_name}}.extensions import db
from {{cookiecutter.app_name}}.commons.pagination import paginate
import logging

logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__, url_prefix='/api/v1')


class UserResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user: UserSchema
        404:
          description: user does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user deleted
        404:
          description: user does not exists
    """

    method_decorators = [jwt_required]

    def get(self, user_id):
        schema = UserSchema()
        user = User.query.get(user_id)
        if user:
            ret = {"data": schema.dump(user.__dict__)}
            return  return_code.SUCCESS.set_data(schema.dump(user.__dict__)), 200
        else:
            return return_code.NOT_FOUND.d, 200

    def put(self, user_id):
        session = db.session
        schema = UserSchema(partial=True)
        user = User.query.get(user_id)
        user = schema.load(request.json, instance=user)
        session.merge(user)
        # session.flush()

        return return_code.SUCCESS.d, 200

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            # db.session.flush()
        else:
            return return_code.NOT_FOUND.d, 200
        return return_code.SUCCESS.d, 200


class UserList(Resource):
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
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user: UserSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        data = {"data": paginate(query, schema)}
        return return_code.SUCCESS.set_data(paginate(query, schema)).d, 200

    def post(self):
        schema = UserSchema(unknown=True)
        user = schema.load(request.json)
        db.session.add(user)
        # db.session.flush()
        return return_code.SUCCESS.d, 200


class UserInfo(Resource):
    method_decorators = [jwt_required]

    def get(self):
        user = get_current_user()
        session = db.session
        session.refresh(user)
        # user.roles = [user.roles]
        schema = UserSchema(unknown=True)
        if user:
            return return_code.SUCCESS.set_data(schema.dump(user.__dict__)).d, 200
        else:
            return return_code.USER_NOT_FOUND.d, 200


@user_bp.route('/users/list', methods=['POST'])
@jwt_required
def export_list():
    query = User.query
    schema = UserSchema(many=True)
    datas = query.all()
    is_or_not_map = common_fun.get_dict_map(const.IS_OR_NOT_DICT_KEY)
    for r in datas:
        r.is_caiyin = is_or_not_map.get(str(r.is_caiyin), r.is_caiyin)
    return return_code.SUCCESS.set_data(schema.dump(datas)).d, 200


{%- if cookiecutter.use_excel == "yes" %}
@user_bp.route('/users/import', methods=['POST'])
@jwt_required
def import_excel():
    session = db.session
    column_names = ['id', 'pwd']
    records = request.get_records(field_name='file', name_columns_by_row=-1, start_row=1, auto_detect_int=False, colnames=column_names)
    is_or_not_map = common_fun.get_revert_dict_map(const.IS_OR_NOT_DICT_KEY)
    # for r in records:
        # r['isCaiyin'] = is_or_not_map.get(str(r['isCaiyin']), r['isCaiyin'])
    db_util.increment_update(session=session,
                             data_dict_list=records,
                             schema_type=UserSchema,
                             is_src=True,
                             request_id=get_jwt_identity())
    # session.flush()
    return return_code.SUCCESS.d, 200
{%- endif %}