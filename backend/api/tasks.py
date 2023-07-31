import json
from datetime import datetime
from io import BytesIO

from PIL import Image

from .celery_worker import celery_app
from .models.photo_model import Photo
from config.redis_config import redis_client


# Apply a simple black-and-white filter
@celery_app.task
def process_photo(photo_bytes, user_id):
    try:
        image = Image.open(BytesIO(photo_bytes))

        bw_image = image.convert('L')

        output_buffer = BytesIO()
        bw_image.save(output_buffer, format='JPEG')
        processed_photo_bytes = output_buffer.getvalue()

        photo_id = redis_client.incr('photo_id')
        original_photo_url = f'/photos/original/{photo_id}.jpg'
        processed_photo_url = f'/photos/processed/{photo_id}.jpg'
        timestamp = str(datetime.now())

        photo = Photo(id=photo_id, user_id=user_id, original_photo_url=original_photo_url,
                      processed_photo_url=processed_photo_url, timestamp=timestamp, )
        photo_dict = photo.to_dict()
        redis_client.set(f'photo:{photo_id}', json.dumps(photo_dict))

        return photo.to_dict(), processed_photo_bytes

    except Exception as e:
        raise e
