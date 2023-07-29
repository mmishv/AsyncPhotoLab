from celery import Celery

app = Celery('photo_queue_project', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')

app.conf.task_default_queue = 'default'
