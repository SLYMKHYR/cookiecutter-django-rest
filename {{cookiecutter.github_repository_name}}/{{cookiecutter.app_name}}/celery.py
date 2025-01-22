import os
from logging import Logger

from celery import Celery
from celery.utils.log import get_task_logger

logger: Logger = get_task_logger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "{{ cookiecutter.app_name }}.settings")
app = Celery("{{ cookiecutter.app_name }}")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
# Discover modules with shared_task
#app.autodiscover_tasks(['aggregator.providers'])
