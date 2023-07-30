from celery import Celery

celery_app = Celery('photo_queue_project', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')

celery_app.conf.task_default_queue = 'default'
