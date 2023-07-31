import os

from celery import Celery

os.environ.setdefault('CELERY_CONFIG_MODULE', 'config.celeryconfig')

celery_app = Celery('photo_queue_project', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')

celery_app.conf.task_default_queue = 'default'

celery_app.config_from_envvar('CELERY_CONFIG_MODULE')
