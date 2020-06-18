from flask.blueprints import Blueprint
import logging
from marshmallow import ValidationError

from {{cookiecutter.app_name}}.commons.constants import return_code
from {{cookiecutter.app_name}}.commons.exception import C

err_bp = Blueprint('error', __name__)

logger = logging.getLogger(__name__)


@err_bp.app_errorhandler(404)
def handle_404(error):
    # logger.exception(error)
    return return_code.PAGE_NOT_FOUND.d, 404


@err_bp.app_errorhandler(405)
def handle_405(error):
    return return_code.METHOD_NOT_ALLOWED.d, 405


@err_bp.app_errorhandler(500)
def handle_500(error):
    logger.exception(error)
    args = list(error.args)
    if len(args) == 0:
        data = error.description
    else:
        data = error.args
    return return_code.UNKNOWN_ERROR.set_data(error.args).d, 500


@err_bp.app_errorhandler(ValidationError)
def handle_validate_error(error):
    logger.exception(error)
    return return_code.PARAM_ILLEGAL.set_data(error.args).d, 200


@err_bp.app_errorhandler(C)
def handle_biz_exception(error):
    logging.exception(error)
    return error, 500


@err_bp.app_errorhandler(Exception)
def handle_exception(error):
    logging.exception(error)
    args = list(error.args)
    if len(args) == 0:
        data = error.description
    else:
        data = error.args
    return return_code.UNKNOWN_ERROR.set_data(data).d, 500
