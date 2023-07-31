from fastapi import APIRouter, UploadFile
from starlette.responses import JSONResponse

from api.tasks import process_photo
from .result import get_processed_photos
from config.settings import UPLOAD_DIR, redis_client
from ..utils.redisdb import remove_old_photos

router = APIRouter()


@router.post("/upload/")
async def upload_photo(file: UploadFile, user_id: int = 1):
    if file.content_type.startswith('image/'):
        photo_bytes = await file.read()

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
        redis_client.delete('processed_photos')
        await get_processed_photos()
        return {"message": "Фотография успешно загружена и поставлена в очередь на обработку.",
                "task_id": task_result['id']}
    else:
        return JSONResponse(status_code=400, content={"detail": "Загруженный файл не является изображением."})
