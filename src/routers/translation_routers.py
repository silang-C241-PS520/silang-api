from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

from ..schemas import auth_schemas
from ..schemas.translation_schemas import TranslationBase, TranslationRead, FeedbackUpdate
from ..services.auth_services import get_current_user
from ..services.translation_services import TranslationServices
from ..utils import get_db
from ..crud.translation_crud import TranslationCRUD
from ..exceptions.translation_exceptions import raise_translation_not_found_exception, raise_forbidden_exception

router = APIRouter(
    prefix="/api/v1/translations",
    tags=["Translation"],
)


@router.get(
    "/me",
    response_model=list[TranslationBase],
    responses={
        200: {
            "description": "Succesfully retrieved translation history",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "video_url": "https://storage.googleapis.com/translation_url_example",
                        "translation_text": "Saya",
                        "date_time_created": "2024-06-19T06:37:58.752Z",
                        "feedback": "Translation feedback"
                    }
                }
            }
        },
        404: {
            "description": "Translation not found",
            "content": {
                "application/json": {
                    "example": "Translation not found."
                }
            }
        }
    }
)
def get_current_user_translations(
        current_user: Annotated[auth_schemas.UserRead, Depends(get_current_user)],
        db: Session = Depends(get_db)
):
    """
    Returns the current user's translations ordered by the most recent.
    """
    current_user_id = current_user.id

    translation_crud = TranslationCRUD(db)

    if not translation_crud.get_sorted_translations_by_user_id(current_user_id):
        raise_translation_not_found_exception()

    return translation_crud.get_sorted_translations_by_user_id(current_user_id)


@router.get(
    "/{id}",
    response_model=TranslationBase,
    responses={
        200: {
            "description": "Succesfully retrieved translation",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "video_url": "https://storage.googleapis.com/translation_url_example",
                        "translation_text": "Saya",
                        "date_time_created": "2024-06-19T06:37:58.752Z",
                        "feedback": "Translation feedback"
                    }
                }
            }
        },
        403: {
            "description": "Access to this resource is not allowed.",
            "content": {
                "application/json": {
                    "example": "Access to this resource is not allowed."
                }
            }
        },
        404: {
            "description": "Translation not found",
            "content": {
                "application/json": {
                    "example": "Translation not found."
                }
            }
        },
    }
)
def get_translation_by_id(
        id: int,
        current_user: Annotated[auth_schemas.UserRead, Depends(get_current_user)],
        db: Session = Depends(get_db)
):
    translation_crud = TranslationCRUD(db)

    if not translation_crud.get_by_id(id):
        raise_translation_not_found_exception()

    if translation_crud.get_by_id(id).user_id != current_user.id:
        raise_forbidden_exception()

    return translation_crud.get_by_id(id)


@router.post(
    "/",
    status_code=201,
    response_model=TranslationRead,
    responses={
        201: {
            "description": "Translation created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "video_url": "https://storage.googleapis.com/translation_url_example",
                        "translation_text": "Saya",
                        "date_time_created": "2024-06-19T06:37:58.752Z",
                        "feedback": None,
                        "user_id": 1
                    }
                }
            }
        },
        413: {
            "description": "Request entity too large",
            "content": {
                "application/json": {
                    "example": "Request entity too large."
                }
            }
        },
        415: {
            "description": "Unsupported media type",
            "content": {
                "application/json": {
                    "example": "Unsupported media type."
                }
            }
        }
    }
)
def create_translation(
        file: UploadFile,
        current_user: Annotated[auth_schemas.UserRead, Depends(get_current_user)],
        db: Session = Depends(get_db)
):
    service = TranslationServices(db)
    return service.create_translation(file, current_user)


# udh barengan get translation
# @router.get(
#     "/{id}/feedbacks",
#     response_model=TranslationRead,
#     responses={
#         200: {"description": "Get feedback by id"},
#         404: {"description": "Translation not found"}
#     }
# )
# async def get_feedback_by_id(id: int, current_user: Annotated[str, Depends(oauth2_scheme)] = Depends(get_current_user)):
#     # TODO
#     return TranslationRead(id=1, video_url="video_url", translation_text="translation_text", date_time_created="", feedback="feedback")


@router.put(
    "/{id}/feedbacks",
    response_model=TranslationRead,
    responses={
        200: {
            "description": "Feedback updated",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "video_url": "https://storage.googleapis.com/translation_url_example",
                        "translation_text": "Saya",
                        "date_time_created": "2024-06-19T06:37:58.752Z",
                        "feedback": "Updated feedback",
                        "user_id": 1
                    }
                }
            }
        },
        404: {
            "description": "Translation not found",
            "content": {
                "application/json": {
                    "example": "Translation not found."
                }
            }
        }
    }
)
def update_feedback_by_id(
        id: int,
        feedback: FeedbackUpdate,
        current_user: Annotated[auth_schemas.UserRead, Depends(get_current_user)],
        db: Session = Depends(get_db)
):
    service = TranslationServices(db)
    return service.update_feedback_by_id(id, feedback, current_user)