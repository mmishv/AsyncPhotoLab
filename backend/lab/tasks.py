from datetime import datetime
from PIL import Image
from io import BytesIO
import base64
from celery_worker import celery_app

import redis

from lab.models import Photo

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# Apply a simple black-and-white filter
@celery_app.task
def process_photo(user_id, photo_bytes):
    try:
        image = Image.open(BytesIO(photo_bytes))

        bw_image = image.convert('L')

        output_buffer = BytesIO()
        bw_image.save(output_buffer, format='JPEG')
        processed_photo_bytes = output_buffer.getvalue()

        processed_photo_base64 = base64.b64encode(processed_photo_bytes).decode('utf-8')

        photo_id = redis_client.incr('photo_id')
        original_photo_url = f'/photos/original/{photo_id}.jpg'
        processed_photo_url = f'/photos/processed/{photo_id}.jpg'
        timestamp = str(datetime.now())

        photo = Photo(
            id=photo_id,
            user_id=user_id,
            original_photo_url=original_photo_url,
            processed_photo_url=processed_photo_url,
            timestamp=timestamp,
            processed_photo_base64=processed_photo_base64
        )
        redis_client.set(f'photo:{photo_id}', photo.model_dump_json())

        import time
        time.sleep(5)

        return photo

    except Exception as e:
        raise e
