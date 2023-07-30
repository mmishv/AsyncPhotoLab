import base64
import json
from pathlib import Path

import redis
from fastapi import UploadFile, HTTPException, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from .tasks import process_photo
import io


app = FastAPI()

origins = ["http://localhost", "http://localhost:3000", "http://localhost:8000", ]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

UPLOAD_DIR = Path("photos")


@app.post("/upload/")
async def upload_photo(file: UploadFile, user_id: int = 1):
    try:
        if file.content_type.startswith('image/'):

            photo_bytes = await file.read()

            result = process_photo.delay(photo_bytes, user_id)
            task_result, processed_photo_bytes = result.get()

            original_photo_path = UPLOAD_DIR / f"{task_result['id']}_{task_result['timestamp']}_original.jpg"
            processed_photo_path = UPLOAD_DIR / f"{task_result['id']}__{task_result['timestamp']}_processed.jpg"

            UPLOAD_DIR.mkdir(exist_ok=True)
            with original_photo_path.open("wb") as f:
                f.write(photo_bytes)

            with processed_photo_path.open("wb") as f:
                f.write(processed_photo_bytes)

            return {"message": "Фотография успешно загружена и поставлена в очередь на обработку.",
                    "task_id": task_result['id']}

        else:
            raise HTTPException(status_code=400, detail="Загруженный файл не является изображением.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")


@app.get("/result/{task_id}")
async def get_result(task_id: str):
    try:
        task_result = process_photo.AsyncResult(task_id)

        if task_result.ready():
            if task_result.successful():
                photo_path = UPLOAD_DIR / f"{task_id}_processed.jpg"

                with photo_path.open("rb") as f:
                    processed_photo_bytes = f.read()

                return {"message": "Фотография успешно обработана.", "download_link": f"/download/{task_id}"}

            else:
                raise HTTPException(status_code=500, detail="Ошибка при обработке фотографии.")

        else:
            return {"message": "Обработка фотографии еще не завершена."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")


@app.get("/download/{task_id}")
async def download_result(task_id: str):
    try:
        task_result = process_photo.AsyncResult(task_id)

        if task_result.ready() and task_result.successful():
            photo_path = UPLOAD_DIR / f"{task_id}_processed.jpg"

            with photo_path.open("rb") as f:
                processed_photo_bytes = f.read()

            return StreamingResponse(io.BytesIO(processed_photo_bytes), media_type="image/jpeg",
                                     headers={"Content-Disposition": f"attachment; filename=processed_{task_id}.jpg"})

        else:
            raise HTTPException(status_code=404, detail="Результат обработки фотографии не найден.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")


@app.get("/photos/processed/")
async def get_processed_photos():
    try:
        processed_photos = []
        for photo_path in UPLOAD_DIR.glob("*_processed.jpg"):
            photo_id = photo_path.stem.split('_')[0]
            timestamp = photo_path.stem.split('_')[-2]
            with photo_path.open("rb") as f:
                photo_bytes = f.read()
                photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
                processed_photos.append({"id": int(photo_id), "photo_bytes": photo_base64, 'timestamp': timestamp})

        return json.dumps(processed_photos)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")
