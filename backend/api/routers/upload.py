from fastapi import APIRouter, UploadFile, Header
from starlette.responses import JSONResponse

from ...api.tasks import process_photo
from ..config.upload_config import UPLOAD_DIR
from .result import get_processed_photos
from ..config.redis_config import redis_client
from ..utils.redisdb import remove_old_photos
from ..utils.user import get_user_by_email

router = APIRouter()


@router.post("/upload/")
async def upload_photo(file: UploadFile, email: str = Header(None)):
    if file.content_type.startswith('image/'):
        photo_bytes = await file.read()

        user = get_user_by_email(email)
        user_id = 0 if user is None else user.id
        result = process_photo.delay(photo_bytes, user_id)
        task_result, processed_photo_bytes = result.get()

        original_photo_path = UPLOAD_DIR / f"{task_result['id']}_original.jpg"
        processed_photo_path = UPLOAD_DIR / f"{task_result['id']}_processed.jpg"

        UPLOAD_DIR.mkdir(exist_ok=True)
        with original_photo_path.open("wb") as f:
            f.write(photo_bytes)

        with processed_photo_path.open("wb") as f:
            f.write(processed_photo_bytes)

        await remove_old_photos()
        redis = await redis_client()
        await redis.delete('processed_photos')
        await get_processed_photos()
        return {"message": "Фотография успешно загружена и поставлена в очередь на обработку.",
                "task_id": task_result['id']}
    else:
        return JSONResponse(status_code=400, content={"detail": "Загруженный файл не является изображением."})
