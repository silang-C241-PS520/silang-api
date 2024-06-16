import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.database import Base
from src.utils import get_db
from src.crud import auth_crud
from .database import engine, override_get_db, test_db

@pytest.fixture()
def refresh_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
client.base_url = str(client.base_url) + "/api/v1/auth"


first_registrar_data = {
            "username": "johndoe",
            "password": "secretpassword123",
            "confirm_password": "secretpassword123"
        }

second_registrar_data = {
            "username": "janesmith",
            "password": "secretpassword012",
            "confirm_password": "secretpassword012"
        }

login_data = {
    "username": "johndoe",
    "password": "secretpassword123"
}


def get_auth_header(test_db):
    access_token = auth_crud.get_token_by_user_id(test_db, user_id=1).access_token
    return {"Authorization": f"Bearer {access_token}"}


def test_register_success(refresh_db, test_db):
    response = client.post(
        "/register",
        json=first_registrar_data
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "johndoe"


def test_register_username_exist():
    response = client.post(
        "/register",
        json=first_registrar_data
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Username already exists."


def test_register_insufficient_password_length():
    response = client.post(
        "/register",
        json={**second_registrar_data, "password": "short12"}
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Password must be at least 8 characters."


def test_register_incorrect_password_confirmation():
    response = client.post(
        "/register",
        json={**second_registrar_data, "confirm_password": "wrongconfirmation"}
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Password confirmation does not match."


def test_user_registered_in_db(test_db):
    user_list = auth_crud.get_all_users(test_db)
    assert len(user_list) == 1

    user_object = auth_crud.get_user_by_username(test_db, username="johndoe")
    assert user_object.id == 1
    assert user_object.username == "johndoe"


def test_login_succesful():
    response = client.post(
        "/login",
        data=login_data
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_login_with_wrong_password():
    response = client.post(
        "/login",
        data={**login_data, "password": "wrongpassword"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password."


def test_token_saved_in_db(test_db):
    token_list = auth_crud.get_all_tokens(test_db)
    token_object = auth_crud.get_token_by_user_id(test_db, user_id=1)

    assert len(token_list) == 1
    assert token_object.user_id == 1


def test_logout_with_invalid_token():
    response = client.post(
        "/logout",
        headers={"Authorization": "Bearer"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials."


def test_logout_succesful(test_db):
    response = client.post(
        "/logout",
        headers=get_auth_header(test_db)
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Logged out successfully."
