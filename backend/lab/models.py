from pydantic import BaseModel


class Photo(BaseModel):
    id: int
    original_photo_url: str
    processed_photo_url: str
    timestamp: str
    user_id: int
