import os
from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.orm import Session

from .gcp_storage_services import GCPStorageServices
from ..crud.translation_crud import TranslationCRUD
from ..exceptions.translation_exceptions import raise_translation_not_found_exception, raise_forbidden_exception
from ..schemas.translation_schemas import FeedbackUpdate
from .ml_services import MLServices
from ..schemas.auth_schemas import UserRead
from ..schemas.translation_schemas import TranslationCreate, TranslationRead


class TranslationServices:
    def __init__(self, db: Session):
        self.ml_service = MLServices()
        self.storage_service = GCPStorageServices()
        self.crud = TranslationCRUD(db)

    def create_translation(self, file: UploadFile, user: UserRead) -> TranslationRead:
        self._check_file_valid()

        # do translation
        translation_text = self.ml_service.do_translation(file)

        # store video to google cloud storage
        video_url = self.storage_service.upload_file(file)

        # store translation result to database
        new_translation = TranslationCreate(
            user_id=user.id,
            video_url=video_url,
            translation_text=translation_text,
            date_time_created=datetime.now()
        )
        return self.crud.store_translation(new_translation)

    def update_feedback_by_id(self, id: int, feedback: FeedbackUpdate, user: UserRead) -> TranslationRead:
        translation = self.crud.get_by_id(id)

        if not translation:
            raise_translation_not_found_exception()

        if translation.user_id != user.id:
            raise_forbidden_exception()

        translation.feedback = feedback.feedback
        self.crud.update_translation(translation)
        return translation

    def _check_file_valid(self):
        # TODO
        pass
