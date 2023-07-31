import logging

from fastapi import HTTPException, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from .routers.download import router as download_router
from .routers.result import router as result_router
from .routers.upload import router as upload_router
from .routers.auth import router as auth_router
from config.settings import origins

app = FastAPI()

logging.basicConfig(level=logging.ERROR)


@app.exception_handler(Exception)
async def http_exception_handler(request, exc):
    logging.error(f"Произошла ошибка на сервере: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Произошла ошибка на сервере."})


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logging.error(f"Ошибка HTTP: {exc}")
    status_code = exc.status_code if isinstance(exc, HTTPException) else 500
    detail = exc.detail if isinstance(exc, HTTPException) else str(exc)
    return JSONResponse(status_code=status_code, content={"detail": detail})


app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )

app.add_exception_handler(Exception, http_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(upload_router)
app.include_router(result_router)
app.include_router(download_router)
app.include_router(auth_router)
