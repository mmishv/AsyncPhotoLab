from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/upload/")
async def upload_photo(file: UploadFile = File(...)):
    # file_path = save_uploaded_file(file)
    # process_photo.delay(file_path)
    return {"message": "Фотография успешно загружена и поставлена в очередь на обработку."}
