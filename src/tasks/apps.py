import logging
import os

from celery import Celery
from django.apps import AppConfig


logger = logging.getLogger(__name__)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('shop')


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        app.config_from_object('django.conf:settings', namespace='CELERY')
        app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    from celery.utils.log import base_logger
    base_logger = base_logger

    base_logger.debug('debug message')
    base_logger.info('info message')
    base_logger.warning('warning message')
    base_logger.error('error message')
    base_logger.critical('critical message')

    logger.debug('Request: {0!r}'.format(self.request))

    return 42
