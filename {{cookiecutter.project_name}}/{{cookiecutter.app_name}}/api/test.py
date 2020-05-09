from flask import Blueprint
import logging

from {{cookiecutter.app_name}}.commons.constants import return_code
from {{cookiecutter.app_name}}.tasks.example import dummy_task

logger = logging.getLogger(__name__)


blueprint = Blueprint('test', __name__, url_prefix='/api/v1')


@blueprint.route('/test', methods=['POST'])
def test():
    logger.debug('call debug test')
    logger.info('call info test')
    logger.warning('call warning test')
    logger.error('call error test')
    return return_code.SUCCESS.d, 200


@blueprint.route("/test1", methods=['GET'])
def test_celery():
    dummy_task.delay('ABINBEV_ZIY_FAC', ())
    return return_code.SUCCESS.d, 200
