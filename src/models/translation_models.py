from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from ..database import Base


class TranslationResult(Base):
    __tablename__ = "translation_results"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"), index=True)
    video_url = Column(String)
    translation_text = Column(String)
    translation_date = Column(DateTime)
    feedback = Column(Text, nullable=True)
