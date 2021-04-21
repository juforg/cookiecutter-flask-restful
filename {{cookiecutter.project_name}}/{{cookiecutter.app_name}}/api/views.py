from flask import Blueprint, current_app
from flask_restful import Api
from {{cookiecutter.app_name}}.extensions import apispec
from {{cookiecutter.app_name}}.api.resources import UserResource, UserList
from {{cookiecutter.app_name}}.api.schemas.user import UserSchema
from {{cookiecutter.app_name}}.api.resources.user import UserInfo
from {{cookiecutter.app_name}}.api.resources.dict import DictResource, DictList, DictSchema
from {{cookiecutter.app_name}}.api.resources.dict_item import DictItemResource, DictItemList, DictItemSchema

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

api.add_resource(UserInfo, '/user/info')
api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(DictResource, '/dict/<int:id>')
api.add_resource(DictList, '/dicts')
api.add_resource(DictItemResource, '/dict_item/<int:id>')
api.add_resource(DictItemList, '/dict_items/<string:dict_code>')

@api_bp.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.components.schema("DictSchema", schema=DictSchema)
    apispec.spec.components.schema("DictItemSchema", schema=DictItemSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.path(view=DictList, app=current_app)
    apispec.spec.path(view=DictResource, app=current_app)
    apispec.spec.path(view=DictItemList, app=current_app)

