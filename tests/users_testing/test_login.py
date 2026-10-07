def test_login_user(client):
    client.post(
        "/user/register",
        json= {
            "username": "testuser02",
            "email": "testuser02@gmail.com",
            "password": "test0000"
        }
    )

    response = client.post(
        "/user/login",
        json= {
            "email": "testuser02@gmail.com",
            "password": "test0000"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "user"
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post(
        "/user/register",
        json= {
            "username": "wrongpassuser",
            "email": "wrongpassuser@gmail.com",
            "password": "test0000"
        }
    )

    response = client.post(
        "/user/login",
        json= {
            "email": "wrongpassuser@gmail.com",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401

def test_non_existent_user(client):
    response = client.post(
        "/user/login",
        json= {
            "email": "nonexistentuser@gmail.com",
            "password": "test0000"
        }
    )

    assert response.status_code == 401
