from flask.blueprints import Blueprint
import logging
from marshmallow import ValidationError

from {{cookiecutter.app_name}}.commons.constants.return_code import ReturnCode
from {{cookiecutter.app_name}}.commons.exception import BizException

err_bp = Blueprint('error', __name__)

logger = logging.getLogger(__name__)


@err_bp.app_errorhandler(404)
def handle_404(error):
    # logger.exception(error)
    return ReturnCode.PAGE_NOT_FOUND, 404


@err_bp.app_errorhandler(405)
def handle_405(error):
    return ReturnCode.METHOD_NOT_ALLOWED, 405


@err_bp.app_errorhandler(500)
def handle_500(error):
    logger.exception(error)
    args = list(error.args)
    if len(args) == 0:
        data = error.description
    else:
        data = error.args
    data = {"data": error.args}
    return dict(data, **ReturnCode.UNKNOWN_ERROR), 500


@err_bp.app_errorhandler(ValidationError)
def handle_validate_error(error):
    logger.exception(error)
    data = {"data": error.args}
    return dict(data, **ReturnCode.PARAM_ILLEGAL), 200


@err_bp.app_errorhandler(BizException)
def handle_biz_exception(error):
    logging.exception(error)
    return error.dict(), 500


@err_bp.app_errorhandler(Exception)
def handle_exception(error):
    logging.exception(error)
    args = list(error.args)
    if len(args) == 0:
        data = error.description
    else:
        data = error.args
    ret = {"data", data}
    return dict(ret, **ReturnCode.UNKNOWN_ERROR), 500
