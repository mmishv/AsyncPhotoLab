import redis
from fastapi import UploadFile, HTTPException, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from lab.models import Photo
from tasks import process_photo
import io

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000", "http://localhost:8000", ]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.post("/upload/")
async def upload_photo(file: UploadFile, user_id: int = 1):
    try:
        if file.content_type.startswith('image/'):

            photo_bytes = await file.read()

            task_result = process_photo.delay(photo_bytes, user_id)

            return {"message": "Фотография успешно загружена и поставлена в очередь на обработку.",
                    "task_id": task_result.id}

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
                # processed_photo_bytes = task_result.get()

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
            processed_photo_bytes = task_result.get()

            return StreamingResponse(io.BytesIO(processed_photo_bytes), media_type="image/jpeg",
                                     headers={"Content-Disposition": f"attachment; filename=processed_{task_id}.jpg"})

        else:
            raise HTTPException(status_code=404, detail="Результат обработки фотографии не найден.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")


@app.get("/photos/processed/")
async def get_processed_photos():
    try:
        photo_keys = redis_client.keys('photo:*')
        processed_photos = [Photo.parse_raw(redis_client.get(key)) for key in photo_keys]

        return processed_photos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")
