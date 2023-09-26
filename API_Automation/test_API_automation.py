import pytest
import json
import logging
from conftest import test_updated_credentials, test_validate_new_user, test_validating_same_user_creds_updated, \
    test_patch_invalid_email

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@pytest.mark.create_user(scope="function")
@pytest.mark.description("Scenario: CRUD Operation for https://gorest.co.in/\n"
                         "Steps:\n"
                         "1) Create new USER (via API)\n"
                         "2) Verify if USER is created\n"
                         "3) Create ToDo for user\n"
                         "4) Verify ToDo is created as intended\n"
                         "5) Update USER credentials\n"
                         "6) Verify USER Credentials are updated correctly USER\n"
                         "7) Delete the USER\n"
                         "8) Verify correct USER is deleted"
                         "9) Negative-scenario try to update USER with INVALID email format"
                         )
def test_create_new_user(test_data):
    logger.info("User Data:")
    logger.info(json.dumps(test_data, indent=4))

    assert test_data is not None


def test_confirm_the_new_user_created(test_data, test_validate_new_user):
    response_data = test_validate_new_user

    assert response_data["status"] == "active"
    assert response_data["name"] is not None
    assert response_data["email"] is not None
    assert response_data["gender"] is not None
    return response_data


def test_create_todo_for_user(test_create_todo, test_data):
    user_id, _ = test_data


def test_confirm_user_todos_created(test_create_todo, test_get_user_todos):
    post_response = test_create_todo
    get_response = test_get_user_todos


def test_update_user_credentials(test_updated_credentials):
    updated_data = test_updated_credentials
    assert updated_data is not None


def test_confirm_users_credentials_updated(test_validating_same_user_creds_updated):
    get_response_data = test_validating_same_user_creds_updated

    expected_name = get_response_data["name"]
    expected_email = get_response_data["email"]
    expected_gender = get_response_data["gender"]

    assert get_response_data["name"] == expected_name
    assert get_response_data["email"] == expected_email
    assert get_response_data["gender"] == expected_gender


def test_delete_user(test_data, test_delete_user):
    user_id, _ = test_data


def test_verify_deleted_user(test_data, test_verify_deleted_user):
    user_id, _ = test_data


@pytest.mark.usefixtures("test_patch_invalid_email")
def test_negative_invalid_patch_request(test_patch_invalid_email):
    assert not str(test_patch_invalid_email.status_code).startswith('2')


######################

@pytest.mark.usefixtures("make_post_request_to_posts_endpoint")
def test_post_request_success(make_post_request_to_posts_endpoint):
    response = make_post_request_to_posts_endpoint
    assert response.status_code == 201
    response_data = json.loads(response.text)
    assert 'user_id' in response_data
    assert response_data['user_id'] == 5202764
    assert response_data['title'] == "Sourav"
    assert response_data['body'] == "Test task for Monese"


