import os
import sys
import shutil

use_celery = '{{cookiecutter.use_celery}}'
use_apispec = '{{cookiecutter.use_apispec}}'


if use_celery == "no":
    base_path = os.getcwd()
    app_path = os.path.join(
        base_path,
        '{{cookiecutter.app_name}}',
    )
    tasks_path = os.path.join(app_path, 'tasks')
    celery_app_path = os.path.join(app_path, 'celery_app.py')

    try:
        shutil.rmtree(tasks_path)
    except Exception:
        print("ERROR: cannot delete celery tasks path %s" % tasks_path)
        sys.exit(1)

    try:
        os.remove(celery_app_path)
    except Exception:
        print("ERROR: cannot delete celery application file")
        sys.exit(1)

    try:
        os.remove(os.path.join(base_path, "tests", "test_celery.py"))
    except Exception:
        print("ERROR: cannot delete celery tests files")
        sys.exit(1)

if use_apispec == "no":
    base_path = os.getcwd()
    apispec_file_path = os.path.join(
        base_path,
        '{{cookiecutter.app_name}}',
        'commons',
        'apispec.py'
    )

    try:
        os.remove(apispec_file_path)
    except Exception:
        print("ERROR: cannot delete path %s" % apispec_file_path)
        sys.exit(1)