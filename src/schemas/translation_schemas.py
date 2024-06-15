from typing import Union

from pydantic import BaseModel
from datetime import datetime


class TranslationRead(BaseModel):
    id: int
    user_id: int
    video_url: str
    translation_text: str
    date_time_created: datetime
    feedback: Union[str | None]


class TranslationCreate(BaseModel):
    user_id: int
    video_url: str
    translation_text: str
    date_time_created: datetime

    class Config:
        from_attributes = True


class FeedbackUpdate(BaseModel):
    feedback: str
