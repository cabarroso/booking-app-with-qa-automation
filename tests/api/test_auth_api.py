import pytest

@pytest.mark.smoke
@pytest.mark.auth
@pytest.mark.login
def test_login_status(auth_service, valid_login_credentials):
    response = auth_service.login(valid_login_credentials)

    assert response.status_code == 200

@pytest.mark.auth
@pytest.mark.login
def test_login(auth_service, valid_login_credentials):
    response = auth_service.login(valid_login_credentials)

    assert "token" in response.json()

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
