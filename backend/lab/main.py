import base64
import json
from pathlib import Path
import aiofiles
import redis
from fastapi import UploadFile, HTTPException, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, JSONResponse
from .tasks import process_photo

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000", "http://localhost:8000", ]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

UPLOAD_DIR = Path("photos")


@app.post("/upload/")
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

        return {"message": "Фотография успешно загружена и поставлена в очередь на обработку.",
                "task_id": task_result['id']}
    else:
        return JSONResponse(status_code=400, content={"detail": "Загруженный файл не является изображением."})


@app.get("/result/{task_id}")
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


@app.get("/download/{task_id}")
async def download_result(task_id: str):
    photo_path = UPLOAD_DIR / f"{task_id}_processed.jpg"

    if not photo_path.exists():
        return JSONResponse(status_code=404, content={"detail": "Результат обработки фотографии не найден."})

    try:
        return FileResponse(photo_path, media_type="image/jpeg", filename=f"processed_{task_id}.jpg")

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Произошла ошибка: {e}"})


@app.get("/photos/processed/")
async def get_processed_photos():
    try:
        processed_photos = []
        for photo_path in UPLOAD_DIR.glob("*_processed.jpg"):
            photo_id = photo_path.stem.split('_')[0]
            timestamp = json.loads(redis_client.get(f'photo:{photo_id}')).get('timestamp')
            async with aiofiles.open(photo_path, mode='rb') as f:
                photo_bytes = await f.read()
                photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
                processed_photos.append({"id": int(photo_id), "photo_bytes": photo_base64, 'timestamp': timestamp})

        return json.dumps(processed_photos)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")
