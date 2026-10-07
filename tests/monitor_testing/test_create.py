def test_create_monitor(client):
    client.post(
        "/user/register",
        json={
            "username": "monitoruser",
            "email": "monitoruser@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "monitoruser@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.post(
        "/monitor/new_monitor",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "product_link": "https://example.com/product1",
            "threshold": 500.00
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["monitor_id"] is not None
    assert data["product_link"] == "https://example.com/product1"
    assert float(data["threshold"]) == 500.00
    assert data["status"] == "active"

def test_duplicate_monitor(client):
    client.post(
        "/user/register",
        json={
            "username": "duplicateuser",
            "email": "duplicateuser@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "duplicateuser@gmail.com",
            "password": "test0000"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    payload = {
        "product_link": "https://example.com/product1",
        "threshold": 500.00
    }

    response_1 = client.post(
        "/monitor/new_monitor",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=payload
    )

    response_2 = client.post(
        "/monitor/new_monitor",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=payload
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 409

def test_invalid_threshold(client):
    client.post(
        "/user/register",
        json={
            "username": "invalidmonitor",
            "email": "invalidmonitor@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "invalidmonitor@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.post(
        "/monitor/new_monitor",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "product_link": "https://example.com/product1",
            "threshold": -100
        }
    )

    assert response.status_code == 422
