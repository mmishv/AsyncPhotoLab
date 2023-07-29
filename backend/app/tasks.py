# tasks.py
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/0')

@app.task
def process_photo(photo_url):
    # processed_photo = apply_filters(photo_url)
    # save_to_redis(photo_url, processed_photo)
    pass
