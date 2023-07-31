import base64
import json
from datetime import timedelta

import aiofiles
from fastapi import HTTPException

from config.settings import MAX_FILES_IN_UPLOAD_DIR, UPLOAD_DIR, redis_client


async def remove_old_photos():
    processed_photos = list(UPLOAD_DIR.glob("*_processed.jpg"))
    if len(processed_photos) > MAX_FILES_IN_UPLOAD_DIR:
        processed_photos.sort(key=lambda x: x.stat().st_mtime)
        for old_photo in processed_photos[:len(processed_photos) - MAX_FILES_IN_UPLOAD_DIR]:
            old_photo.unlink()
            photo_id = old_photo.stem.split('_')[0]
            redis_client.delete(f'photo:{photo_id}')


async def get_photos(user_id: int = None):
    try:
        processed_photos = []
        for photo_path in UPLOAD_DIR.glob("*_processed.jpg"):
            photo_id = photo_path.stem.split('_')[0]
            photo = json.loads(redis_client.get(f'photo:{photo_id}'))
            timestamp = photo.get('timestamp')
            if user_id is not None and photo.get('user_id') != user_id:
                continue
            async with aiofiles.open(photo_path, mode='rb') as f:
                photo_bytes = await f.read()
                photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
                photo_data = {"id": int(photo_id), "photo_bytes": photo_base64, "timestamp": timestamp}
                processed_photos.append(photo_data)

        redis_client.setex('processed_photos', timedelta(minutes=1), json.dumps(processed_photos))
        return json.dumps(processed_photos)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")


async def get_cached_processed_photos():
    cached_photos = redis_client.get('processed_photos')
    if cached_photos:
        return json.loads(cached_photos)

    processed_photos = await get_photos()

    redis_client.setex('processed_photos', timedelta(minutes=1), json.dumps(processed_photos))
    return processed_photos
