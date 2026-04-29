import pytest
import allure

@allure.title("API Login - Successful Login")
@allure.description("API Login - Posting with valid credentials results in successful response with a login token.")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.api
@pytest.mark.auth
@pytest.mark.login
def test_login_status_200(auth_service, valid_login_credentials):
    with allure.step("Login with valid credentials."):
        response = auth_service.login(valid_login_credentials)

    with allure.step("Verify 200 status code in response."):
        assert response.status_code == 200

    with allure.step("Verify 'token' is in response payload."):
        assert "token" in response.json()

@allure.title("API Login - Failed Login with Wrong Credentials")
@allure.description("Posting with wrong credentials (but valid value type) results in status code 401 with no token.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.auth
@pytest.mark.login
@pytest.mark.parametrize("credentials", 
                        [{"username": "wrong_username", "password": "password123"},
                         {"username": "admin", "password": "wrong_password"}],
                        ids=["username", "password"])
def test_login_wrong_credentials(auth_service, credentials):
    with allure.step("Attempt login with wrong credentials"):
        response = auth_service.login(credentials)

    with allure.step("Verify response status 401"):
        assert response.status_code == 401

    with allure.step("Verify 'token' is not present in response payload"):
        assert "token" not in response.json()

@allure.title("API Login - Failed Login with Invalid Input Types")
@allure.description("Posting with invalid field value types results in status code 422 with no token.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.auth
@pytest.mark.login
@pytest.mark.parametrize("credentials", 
                        [{"username": 1337, "password": "password123"},
                         {"username": "admin", "password": False}],
                        ids=["username", "password"])
def test_login_invlid_field_type(auth_service, credentials):

    with allure.step("Attempt login with invalid value types"):
        response = auth_service.login(credentials)

    with allure.step("Verify response status of 422"):
        assert response.status_code == 422

    with allure.step("Verify 'token' not present in response payload"):
        assert "token" not in response.json()