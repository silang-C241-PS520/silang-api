from pydantic import BaseModel
from datetime import datetime


class TranslationRead(BaseModel):
    id: int
    video_url: str
    translation_text: str
    translation_date: datetime
    feedback: str | None


class FeedbackUpdate(BaseModel):
    feedback: str
