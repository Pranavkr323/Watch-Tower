def test_get_profile(client):
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
    token = response.json()["access_token"]

    profile_response = client.get(
        "/user/testuser02",
        headers= {
            "Authorization" : f"Bearer {token}"
        }
    )

    assert profile_response.status_code == 200
    data = profile_response.json()
    assert data["username"] == "testuser02"
    assert data["email"] == "testuser02@gmail.com"

def test_get_other_profile(client):
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
    token = response.json()["access_token"]

    profile_response = client.get(
        "/user/testuser01",
        headers= {
            "Authorization" : f"Bearer {token}"
        }
    )

    assert profile_response.status_code == 403

def test_update_profile(client):
    client.post(
        "/user/register",
        json= {
            "username": "notupdateuser02",
            "email": "notupdateuser02@gmail.com",
            "password": "test0000"
        }
    )

    response = client.post(
        "/user/login",
        json= {
            "email": "notupdateuser02@gmail.com",
            "password": "test0000"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    profile_response = client.patch(
        "/user/notupdateuser02",
        headers= {
            "Authorization" : f"Bearer {token}"
        },
        json= {
            "username": "updateuser",
            "email": "updateuser02@gmail.com"
        }
    )

    assert profile_response.status_code == 200
    data = profile_response.json()

    assert data["username"] == "updateuser"
    assert data["email"] == "updateuser02@gmail.com"

def test_update_other_profile(client):
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
    token = response.json()["access_token"]

    profile_response = client.patch(
        "/user/testuser01",
        headers= {
            "Authorization" : f"Bearer {token}"
        },
        json= {
            "username": "updateuser01",
            "email": "updateuser01@gmail.com"
        }
    )

    assert profile_response.status_code == 403
