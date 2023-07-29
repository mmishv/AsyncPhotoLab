from fastapi import FastAPI, File, UploadFile
from celery import Celery
from tasks import process_photo

app = FastAPI()

@app.post("/upload/")
async def upload_photo(file: UploadFile = File(...)):
    # Здесь вы можете сохранить загруженный файл и вызвать задачу Celery для обработки фотографии
    # Пример:
    # file_path = save_uploaded_file(file)
    # process_photo.delay(file_path)
    return {"message": "Фотография успешно загружена и поставлена в очередь на обработку."}
