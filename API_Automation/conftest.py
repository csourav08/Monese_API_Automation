
import pytest
import requests
from faker import Faker
import logging
import json

fake = Faker()

BASE_URL = 'https://gorest.co.in/public/v2/users/'
ACCESS_TOKEN = 'a6feb1e9909e836edaa64ebb91544d694441cb09f1bc0940fe3f11f568aa191f'


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'filename': record.filename,
            'lineno': record.lineno,
        }
        return json.dumps(log_data)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
log_file_path = 'debug_logs.json'
file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
json_formatter = JsonFormatter()
file_handler.setFormatter(json_formatter)
logger.addHandler(file_handler)

def get_headers():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }

@pytest.fixture(scope="module")
def test_data():
    headers = get_headers()


    data = {
        'name': fake.name(),
        'gender': fake.random_element(elements=('male', 'female')),
        'email': fake.email(),
        'status': 'active'
    }
    response = requests.post(BASE_URL, json=data, headers=headers)
    assert response.status_code == 201
    response_data = response.json()


    user_id = response_data["id"]


    logger.debug(f"User created with ID: {user_id}")
    logger.debug(f"User data: {response_data}")

    yield user_id, response_data

@pytest.fixture(scope="function")
def test_validate_new_user(test_data):
    user_id, post_data = test_data
    headers = get_headers()

    response = requests.get(f'{BASE_URL}/{user_id}', headers=headers)
    assert response.status_code == 200
    response_data = response.json()


    logger.debug(f"Validating user with ID: {user_id}")
    logger.debug(f"Response data: {response_data}")


    assert response_data["id"] == user_id
    assert response_data["email"] == post_data["email"]
    assert response_data["name"] == post_data["name"]

    return response_data

@pytest.fixture(scope="function")
def test_updated_credentials(test_data):
    user_id, post_data = test_data
    headers = get_headers()

    test_data = {
        'name': fake.name(),
        'gender': fake.random_element(elements=('male', 'female')),
        'email': fake.email(),
        'status': 'active'
    }

    response = requests.patch(f'{BASE_URL}/{user_id}', json=test_data, headers=headers)
    assert response.status_code == 200
    patch_response_data = response.json()
    logger.debug(f"User created with ID: {user_id}")
    logger.debug(f"User data: {patch_response_data}")
    return patch_response_data

@pytest.fixture(scope="function")
def user_id(test_data):
    user_id, _ = test_data
    return user_id

@pytest.fixture(scope="function")
def test_validating_same_user_creds_updated(user_id):
    headers = get_headers()
    response = requests.get(f'{BASE_URL}/{user_id}', headers=headers)
    assert response.status_code == 200
    logger.debug(f"User created with ID: {user_id}")
    logger.debug(f"User data: {response.json()}")
    return response.json()

@pytest.fixture(scope="function")
def test_delete_user(user_id):
    headers = get_headers()

    response = requests.delete(f'{BASE_URL}/{user_id}', headers=headers)

    assert response.status_code == 204
    logger.debug(f"Deleting user with ID: {user_id}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response data: {response.text}")
    return response

@pytest.fixture(scope="function")
def test_verify_deleted_user(user_id):
    headers = get_headers()

    response = requests.get(f'{BASE_URL}/{user_id}', headers=headers)

    logger.debug(f"Verifying user with ID: {user_id}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response data: {response.text}")

    if response.status_code == 404:
        response_data = response.json()
        assert response_data.get("message") == "Resource not found"
        return response


    logger.debug(f"User exists with ID: {user_id}, proceeding with DELETE request")

    delete_response = requests.delete(f'{BASE_URL}/{user_id}', headers=headers)

    assert delete_response.status_code == 204
    logger.debug(f"Deleting user with ID: {user_id}")
    logger.debug(f"DELETE Response status code: {delete_response.status_code}")
    logger.debug(f"DELETE Response data: {delete_response.text}")

    return delete_response

@pytest.fixture(scope="function")
def test_create_todo(user_id):
    headers = get_headers()

    todo_data = {
        "title": fake.sentence(),
        "status": fake.random_element(elements=("pending", "completed"))
    }
    response = requests.post(f'{BASE_URL}{user_id}/todos', json=todo_data, headers=headers)

    assert response.status_code == 201
    logger.debug(f"Verifying deleted user with ID: {user_id}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response data: {response.text}")

    return response

@pytest.fixture(scope="function")
def test_get_user_todos(user_id):
    headers = get_headers()

    response = requests.get(f'{BASE_URL}/{user_id}/todos', headers=headers)

    assert response.status_code == 200
    logger.debug(f"Getting user todos for ID: {user_id}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response data: {response.text}")

    return response.json()

@pytest.fixture(scope="function")
def test_patch_invalid_email(test_data):
    user_id, _ = test_data
    headers = get_headers()


    invalid_test_data = {
        'email': 'updateemail.in',
    }

    response = requests.patch(f'{BASE_URL}/{user_id}', json=invalid_test_data, headers=headers)

    assert not str(response.status_code).startswith('2')

    logger.debug(f"Invalid PATCH request for user ID: {user_id}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response data: {response.text}")

    return response

@pytest.fixture(scope="function")
def make_post_request_to_posts_endpoint():
    fake = Faker()
    user_id = 5202764
    message = "Hello Monese test"
    title = "Sourav"
    body = "Test task for Monese"

    data = {
        'user_id': user_id,
        'message': message,
        'title': title,
        'body': body
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer a6feb1e9909e836edaa64ebb91544d694441cb09f1bc0940fe3f11f568aa191f'
    }

    url = 'https://gorest.co.in/public/v2/posts'

    data_json = json.dumps(data)

    response = requests.post(url, headers=headers, data=data_json)

    # Log the request and response information
    logger.debug(f"POST request to {url}")
    logger.debug(f"Headers: {headers}")
    logger.debug(f"Request data: {data_json}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response data: {response.text}")

    return response


@pytest.fixture(scope="function")
def make_post_request_with_validation():
    # Create headers
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer a6feb1e9909e836edaa64ebb91544d694441cb09f1bc0940fe3f11f568aa191f'
    }

    url = 'https://gorest.co.in/public/v2/posts'

    data = {}

    data_json = json.dumps(data)

    response = requests.post(url, headers=headers, data=data_json)

    logger.debug(f"POST request to {url}")
    logger.debug(f"Headers: {headers}")
    logger.debug(f"Request data: {data_json}")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response data: {response.text}")

    return response




