def test_change_password(client):
    client.post(
        "/user/register",
        json={
            "username": "passworduser",
            "email": "passworduser@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "passworduser@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.patch(
        "/user/passworduser/password",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "current_password": "test0000",
            "new_password": "newpassword"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

    response = client.post(
        "/user/login",
        json={
            "email": "passworduser@gmail.com",
            "password": "newpassword"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    response = client.post(
        "/user/login",
        json={
            "email": "passworduser@gmail.com",
            "password": "test0000"
        }
    )

    assert response.status_code == 401

def test_wrong_user_change_password(client):
    client.post(
        "/user/register",
        json={
            "username": "passworduser",
            "email": "passworduser@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "passworduser@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.patch(
        "/user/otheruser/password",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "current_password": "test0000",
            "new_password": "newpassword"
        }
    )

    assert response.status_code == 403

def test_wrong_password_change_password(client):
    client.post(
        "/user/register",
        json={
            "username": "passworduser",
            "email": "passworduser@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "passworduser@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.patch(
        "/user/passworduser/password",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "current_password": "test0001",
            "new_password": "newpassword"
        }
    )

    assert response.status_code == 401
