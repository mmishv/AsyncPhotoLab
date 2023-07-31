from fastapi import APIRouter
from starlette.responses import JSONResponse, FileResponse

from config.settings import UPLOAD_DIR

router = APIRouter()


@router.get("/download/{task_id}")
async def download_result(task_id: str):
    photo_path = UPLOAD_DIR / f"{task_id}_processed.jpg"

    if not photo_path.exists():
        return JSONResponse(status_code=404, content={"detail": "Результат обработки фотографии не найден."})

    try:
        return FileResponse(photo_path, media_type="image/jpeg", filename=f"processed_{task_id}.jpg")

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Произошла ошибка: {e}"})
