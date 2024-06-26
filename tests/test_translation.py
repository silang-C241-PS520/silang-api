import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime
from io import BytesIO

from src.database import Base
from src.main import app
from src.models.translation_models import Translation
from src.schemas.auth_schemas import UserRead
from src.services.auth_services import get_current_user
from src.utils import get_db
from src.services.ml_services import MLServices
from src.services.translation_services import GCPStorageServices
from tests.database import override_get_db, test_db, engine


@pytest.fixture(autouse=True)
def refresh_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client_authenticated():
    def override_auth():
        return UserRead(id=1, username="johndoe")

    app.dependency_overrides[get_current_user] = override_auth
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def client_not_authenticated():
    app.dependency_overrides[get_current_user] = get_current_user
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def add_translations_to_db(test_db: Session):
    translations = [
        Translation(id=1, user_id=1, video_url="url", translation_text="translation", date_time_created=datetime.now()),
        Translation(id=2, user_id=1, video_url="url", translation_text="translation", date_time_created=datetime.now()),
        Translation(id=3, user_id=2, video_url="url", translation_text="translation", date_time_created=datetime.now())
    ]

    test_db.add_all(translations)
    test_db.commit()


def test_create_translation_success(client_authenticated, mocker, freezer):  # freeze time using freezer
    mocker.patch.object(MLServices, "do_translation", return_value="translation_text")
    mocker.patch.object(GCPStorageServices, "upload_file", return_value="https://video_url")

    video_file = ("video.mp4", BytesIO(b"video_file"), "video/mp4")

    response = client_authenticated.post(
        "api/v1/translations/",
        files={"file": video_file}
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == 1
    assert response.json()["translation_text"] == "translation_text"
    assert response.json()["video_url"] == "https://video_url"
    assert response.json()["date_time_created"] == datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert response.json()["feedback"] is None


def test_create_translation_unauthorized(client_not_authenticated):
    video_file = ("video.mp4", BytesIO(b"video_file"), "video/mp4")
    response = client_not_authenticated.post(
        "api/v1/translations/",
        files={"file": video_file}
    )
    assert response.status_code == 401


def test_get_translation_by_id(client_authenticated, add_translations_to_db):
    response = client_authenticated.get("api/v1/translations/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_translation_by_id_forbidden(client_authenticated, add_translations_to_db):
    response = client_authenticated.get("api/v1/translations/3")

    assert response.status_code == 403
    assert response.json()["detail"] == "Access to this resource is not allowed."


def test_get_translation_by_id_not_found(client_authenticated):
    response = client_authenticated.get("api/v1/translations/3")

    assert response.status_code == 404
    assert response.json()["detail"] == "Translation not found."


def test_get_current_user_translations(client_authenticated, add_translations_to_db):
    response = client_authenticated.get("api/v1/translations/me")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_current_user_translations_not_found(client_authenticated):
    response = client_authenticated.get("api/v1/translations/me")

    assert response.status_code == 404
    assert response.json()["detail"] == "Translation not found."


def test_get_current_user_translations_unauthorized(client_not_authenticated):
    response = client_not_authenticated.get("api/v1/translations/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_update_feedback_by_id_success(client_authenticated, add_translations_to_db, freezer):
    feedback_input = "feedback"
    response = client_authenticated.put(
        "api/v1/translations/1/feedbacks",
        json={"feedback": feedback_input}
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["video_url"] == "url"
    assert response.json()["translation_text"] == "translation"
    assert response.json()["feedback"] == feedback_input


def test_update_feedback_by_id_not_authenticated(client_not_authenticated, add_translations_to_db):
    feedback_input = "feedback"
    response = client_not_authenticated.put(
        "api/v1/translations/1/feedbacks",
        json={"feedback": feedback_input}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_update_feedback_by_id_translation_not_found(client_authenticated):
    feedback_input = "feedback"
    response = client_authenticated.put(
        "api/v1/translations/0/feedbacks",
        json={"feedback": feedback_input}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Translation not found."


def test_update_feedback_by_id_not_allowed(client_authenticated, add_translations_to_db):
    feedback_input = "feedback"
    response = client_authenticated.put(
        "api/v1/translations/3/feedbacks",
        json={"feedback": feedback_input}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Access to this resource is not allowed."