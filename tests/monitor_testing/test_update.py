def test_update_monitor(client):
    client.post(
        "/user/register",
        json={
            "username": "updateuser",
            "email": "updateuser@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "updateuser@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/monitor/new_monitor",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "product_link": "https://example.com/product1",
            "threshold": 500.00
        }
    )

    assert create_response.status_code == 200
    monitor_id = create_response.json()["monitor_id"]

    update_response = client.patch(
        f"/monitor/{monitor_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "threshold": 400.00
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["monitor_id"] == monitor_id
    assert float(data["threshold"]) == 400.00
    assert data["product_link"] == "https://example.com/product1"


def test_update_nonexistent_monitor(client):
    client.post(
        "/user/register",
        json={
            "username": "update404",
            "email": "update404@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "update404@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.patch(
        "/monitor/9999",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "threshold": 400.00
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Monitor not Found!"


def test_update_invalid_threshold(client):
    client.post(
        "/user/register",
        json={
            "username": "invalidupdate",
            "email": "invalidupdate@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "invalidupdate@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/monitor/new_monitor",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "product_link": "https://example.com/product1",
            "threshold": 500.00
        }
    )

    assert create_response.status_code == 200
    monitor_id = create_response.json()["monitor_id"]

    response = client.patch(
        f"/monitor/{monitor_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "threshold": -100
        }
    )

    assert response.status_code == 422


def test_update_unauthorized(client):
    client.post(
        "/user/register",
        json={
            "username": "owneruser",
            "email": "owneruser@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "owneruser@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    owner_token = login_response.json()["access_token"]

    create_response = client.post(
        "/monitor/new_monitor",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "product_link": "https://example.com/product1",
            "threshold": 500.00
        }
    )

    assert create_response.status_code == 200
    monitor_id = create_response.json()["monitor_id"]

    client.post(
        "/user/register",
        json={
            "username": "otheruser",
            "email": "otheruser@gmail.com",
            "password": "test0000"
        }
    )

    other_login = client.post(
        "/user/login",
        json={
            "email": "otheruser@gmail.com",
            "password": "test0000"
        }
    )

    assert other_login.status_code == 200
    other_token = other_login.json()["access_token"]

    response = client.patch(
        f"/monitor/{monitor_id}",
        headers={
            "Authorization": f"Bearer {other_token}"
        },
        json={
            "threshold": 300.00
        }
    )

    assert response.status_code == 404
