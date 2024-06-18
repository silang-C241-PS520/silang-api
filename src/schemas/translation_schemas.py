from pydantic import BaseModel
from datetime import datetime


class TranslationBase(BaseModel):
    id: int
    video_url: str
    translation_text: str
    date_time_created: datetime
    feedback: str | None


class TranslationRead(TranslationBase):
    user_id: int

    class Config:
        from_orm = True


class TranslationCreate(BaseModel):
    user_id: int
    video_url: str
    translation_text: str
    date_time_created: datetime

    class Config:
        from_attributes = True


class FeedbackUpdate(BaseModel):
    feedback: str
