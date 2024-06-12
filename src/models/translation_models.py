from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from ..database import Base


class Translation(Base):
    __tablename__ = "translation"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    video_url = Column(String)
    translation_text = Column(String)
    date_time_created = Column(DateTime)
    feedback = Column(Text, nullable=True)
