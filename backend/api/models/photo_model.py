from pydantic import BaseModel


class Photo(BaseModel):
    id: int
    original_photo_url: str
    processed_photo_url: str
    timestamp: str
    user_id: int

    def to_dict(self):
        return {
            'id': self.id,
            'original_photo_url': self.original_photo_url,
            'processed_photo_url': self.processed_photo_url,
            'timestamp': self.timestamp,
            'user_id': self.user_id,
        }
