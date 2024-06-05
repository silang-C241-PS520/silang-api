from pydantic import BaseModel


class TranslationRead(BaseModel):
    id: int
    video_url: str
    translation_text: str
    date_created: str
    feedback: str | None


class FeedbackUpdate(BaseModel):
    feedback: str
