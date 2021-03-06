from flask import request, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)

from {{cookiecutter.app_name}}.models import User
from {{cookiecutter.app_name}}.extensions import pwd_context, jwt \
    {%- if cookiecutter.use_apispec == "yes"%}, apispec {% endif%}
from {{cookiecutter.app_name}}.auth.helpers import revoke_token, is_token_revoked, add_token_to_database
from {{cookiecutter.app_name}}.commons.constants import return_code
import logging

logger = logging.getLogger(__name__)
blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route("/login", methods=["POST"])
def login():
    """Authenticate user and return tokens

    ---
    post:
      tags:
        - auth
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: myuser
                  required: true
                password:
                  type: string
                  example: P4$$w0rd!
                  required: true
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
                  refresh_token:
                    type: string
                    example: myrefreshtoken
        400:
          description: bad request
      security: []
    """
    if not request.is_json:
        return return_code.JSON_PARSE_FAIL.d, 200
    ret = {}
    try:

        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if not username or not password:
            return return_code.USER_NOT_FOUND.d, 200

        user = User.query.filter_by(username=username).first()
        if user is None or not pwd_context.verify(password, user.password):
            return return_code.NAME_PWD_INVALID.d, 200

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        # add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
        # add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])
        ret = {
            'token': access_token,
            'refresh_token': refresh_token
        }
    except BaseException as e:
        logger.exception(e)
        return return_code.UNKNOWN_ERROR.d, 200
    return return_code.SUCCESS.set_data(ret).d, 200



@blueprint.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    """Get an access token from a refresh token

    ---
    post:
      tags:
        - auth
      parameters:
        - in: header
          name: Authorization
          required: true
          description: valid refresh token
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: myaccesstoken
        400:
          description: bad request
        401:
          description: unauthorized
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"access_token": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return return_code.SUCCESS.set_data(ret).d, 200


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required
def revoke_access_token():
    """Revoke an access token

    ---
    delete:
      tags:
        - auth
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return return_code.SUCCESS.d, 200


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_refresh_token_required
def revoke_refresh_token():
    """Revoke a refresh token, used mainly for logout

    ---
    delete:
      tags:
        - auth
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: token revoked
        400:
          description: bad request
        401:
          description: unauthorized
    """
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return return_code.SUCCESS.d, 200


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.get(identity)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)

@jwt.expired_token_loader
def expired_token_callback():
    return return_code.LOGIN_EXPIRED.d, 200

# 无效令牌
@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return return_code.INVALID_TOKEN.set_data(error).d, 200

{%- if cookiecutter.use_apispec == "yes"%}
@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=login, app=app)
    apispec.spec.path(view=refresh, app=app)
    apispec.spec.path(view=revoke_access_token, app=app)
    apispec.spec.path(view=revoke_refresh_token, app=app)
 {% endif%}