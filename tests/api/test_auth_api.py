import pytest
import allure

@allure.title("API Login - Successful Login")
@allure.description("API Login - Posting with valid credentials results in successful response with a login token.")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.api
@pytest.mark.auth
@pytest.mark.login
def test_login_status_200(auth_service, valid_login_credentials):
    response = auth_service.login(valid_login_credentials)
    assert response.status_code == 200

    assert "token" in response.json()

@allure.title("API Login - Failed Login")
@allure.description("Posting with invalid credentials results in status code 400 with no token.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.auth
@pytest.mark.login
@pytest.mark.parametrize("credentials", 
                        [{"username": "wrong", "password": "wrong123"},
                         {"username": 21, "password": False}],
                        ids=["wrong credentials", "invalid type"])
def test_login_fail(auth_service, credentials):
    response = auth_service.login(credentials)

    assert response.status_code >= 400
    assert "token" not in response.json()
