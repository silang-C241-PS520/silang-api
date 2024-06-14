import os
from datetime import datetime
from typing import Annotated

from fastapi import UploadFile, Depends
from sqlalchemy.orm import Session

from .gcp_storage_services import GCPStorageServices
from ..crud.translation_crud import TranslationCRUD
from ..schemas import translation_schemas
from ..models import translation_models
from .ml_services import MLServices
from ..schemas.auth_schemas import UserRead
from ..schemas.translation_schemas import TranslationCreate, TranslationRead


class TranslationServices:
    def __init__(self, db: Session):
        self.ml_service: Annotated[MLServices, Depends(MLServices)] = MLServices()
        self.storage_service: Annotated[GCPStorageServices, Depends(GCPStorageServices)] = GCPStorageServices()
        self.crud = TranslationCRUD(db)
        self.db = db

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

    def _check_file_valid(self):
        # TODO
        pass
