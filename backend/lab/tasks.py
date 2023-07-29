from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@rabbitmq//', backend='redis://redis:6379/0')

@app.task
def process_photo(photo_url):
    # Здесь вы можете добавить код для обработки фотографии
    # Например, применить фильтры или изменить размер фотографии.
    # Результат обработки можно сохранить в Redis.

    # Пример задачи:
    # processed_photo = apply_filters(photo_url)
    # save_to_redis(photo_url, processed_photo)
    pass
