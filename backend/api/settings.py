from pathlib import Path

import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

SECRET_KEY = '1111'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 1

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
UPLOAD_DIR = Path("photos")

MAX_FILES_IN_UPLOAD_DIR = 10

origins = ["http://localhost", "http://localhost:3000", "http://localhost:8000"]

