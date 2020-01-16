from flask import Blueprint, current_app
from flask_restful import Api

from {{cookiecutter.app_name}}.extensions import apispec
from {{cookiecutter.app_name}}.api.resources import UserResource, UserList
from {{cookiecutter.app_name}}.api.resources.user import UserSchema
from {{cookiecutter.app_name}}.api.resources.dict import DictResource, DictList, DictItemResource, DictItemList

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(DictResource, '/dict/<int:id>')
api.add_resource(DictList, '/dicts')
api.add_resource(DictItemResource, '/dict_item/<int:id>')
api.add_resource(DictItemList, '/dict_items/<string:dict_code>')

@api_bp.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
