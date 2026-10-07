def test_register_user(client):
    response = client.post(
        "/user/register",
        json={
            "username": "testuser01",
            "email": "testuser01@gmail.com",
            "password": "test0000"
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert data["user_id"] is not None
    assert data["username"] == "testuser01"

def test_duplicate_register(client):

    payload = {
        "username": "testuser02",
        "email": "testuser02@gmail.com",
        "password": "test0000"
    }

    response_1 = client.post(
        "/user/register",
        json= payload
    )

    response_2 = client.post(
        "/user/register",
        json= payload
    )

    assert response_1.status_code == 201
    assert response_2.status_code == 409

def test_register_invalid_email(client):
    response = client.post(
        "/user/register",
        json= {
            "username": "testuser02",
            "email": "wdjaij@jd",
            "password": "test0000"
        }
    )
    assert response.status_code == 422
