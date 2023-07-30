from pathlib import Path

import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

UPLOAD_DIR = Path("photos")

MAX_FILES_IN_UPLOAD_DIR = 10

origins = ["http://localhost", "http://localhost:3000", "http://localhost:8000", ]