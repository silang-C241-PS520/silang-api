from sqlalchemy.orm import Session

from src.models.translation_models import Translation
from src.schemas.auth_schemas import UserRead
from src.schemas.translation_schemas import TranslationCreate, TranslationRead


class TranslationCRUD:

    def __init__(self, db: Session):
        self.db = db

    def store_translation(self, translation: TranslationCreate) -> TranslationRead:
        db_translation = Translation(
            user_id=translation.user_id,
            video_url=translation.video_url,
            translation_text=translation.translation_text,
            date_time_created=translation.date_time_created
        )
        self.db.add(db_translation)
        self.db.commit()
        self.db.refresh(db_translation)
        return TranslationRead(
            id=db_translation.id,
            user_id=db_translation.user_id,
            video_url=db_translation.video_url,
            translation_text=db_translation.translation_text,
            date_time_created=db_translation.date_time_created,
            feedback=db_translation.feedback
        )

