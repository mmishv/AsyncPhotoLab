from celery import Celery

broker_url = 'amqp://myuser:mypassword@rabbitmq:5672//'
result_backend = 'redis://redis:6379/0'

celery_app = Celery('photo_queue_project', broker=broker_url, backend=result_backend, result_backend=result_backend,
                    broker_connection_retry=True)

celery_app.conf.task_default_queue = 'default'
