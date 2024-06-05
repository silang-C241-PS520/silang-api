from typing import Annotated

from fastapi import APIRouter, Response, status, UploadFile, Body
from ..schemas.translation_schemas import TranslationRead, FeedbackUpdate

router = APIRouter(
    prefix="/api/v1/translation",
    tags=["Translation"],
)


@router.get(
    "/",
    response_model=list[TranslationRead],
    responses={
        200: {"description": "Get all translation"},
    }
)
async def get_all_translation():
    # TODO
    return [TranslationRead(id=1, video_url="video_url", translation_text="translation_text", translation_date="", feedback="feedback")]


@router.get(
    "/{id}",
    response_model=TranslationRead,
    responses={
        200: {"description": "Get translation by id"},
        404: {"description": "Translation not found"}
    }
)
async def get_translation_by_id(id: int):
    # TODO
    return TranslationRead(id=1, video_url="video_url", translation_text="translation_text", translation_date="", feedback="feedback")


@router.post(
    "/",
    status_code=201,
    response_model=TranslationRead,
    responses={
        201: {"description": "Translation created"},
        413: {"description": "Request Entity Too Large"},
        415: {"description": "Unsupported Media Type"}
    }
)
async def create_translation(file: UploadFile):
    return TranslationRead(id=1, video_url="video_url", translation_text="translation_text", translation_date="", feedback="feedback")


@router.get(
    "/{id}/feedbacks",
    response_model=TranslationRead,
    responses={
        200: {"description": "Get feedback by id"},
        404: {"description": "Translation not found"}
    }
)
async def get_feedback_by_id(id: int):
    # TODO
    return TranslationRead(id=1, video_url="video_url", translation_text="translation_text", translation_date="", feedback="feedback")


@router.put(
    "/{id}/feedbacks",
    response_model=TranslationRead,
    responses={
        200: {"description": "Feedback updated"},
        404: {"description": "Translation not found"}
    }
)
async def update_feedback_by_id(id: int, feedback: FeedbackUpdate):
    # TODO
    return TranslationRead(id=1, video_url="video_url", translation_text="translation_text", translation_date="", feedback="feedback")

