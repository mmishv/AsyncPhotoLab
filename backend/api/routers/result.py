import base64
import json

import aiofiles
from fastapi import APIRouter
from starlette.responses import JSONResponse

from config.settings import UPLOAD_DIR
from ..utils.redisdb import get_photos

router = APIRouter()


@router.get("/result/{task_id}")
async def get_result(task_id: str):
    photo_path = UPLOAD_DIR / f"{task_id}_processed.jpg"

    if not photo_path.exists():
        return JSONResponse(status_code=404, content={"detail": "Результат обработки фотографии не найден."})

    try:
        async with aiofiles.open(photo_path, mode='rb') as f:
            photo_bytes = await f.read()
            photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')

        if photo_base64:
            return json.dumps({'result': photo_base64, 'task_id': task_id})
        else:
            return JSONResponse(status_code=404, content={"detail": "Результат обработки фотографии не найден."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Произошла ошибка: {e}"})


@router.get("/photos/processed/")
async def get_processed_photos():
    return await get_photos()
