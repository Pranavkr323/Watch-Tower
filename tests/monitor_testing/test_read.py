def test_get_monitor(client):
    client.post(
        "/user/register",
        json={
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "testuser@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/monitor/new_monitor",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "product_link": "https://example.com/product1",
            "threshold": 500.00
        }
    )

    assert create_response.status_code == 200
    monitor_id = create_response.json()["monitor_id"]

    response = client.get(
        f"/monitor/{monitor_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["monitor_id"] == monitor_id
    assert data["product_link"] == "https://example.com/product1"
    assert float(data["threshold"]) == 500.00

def test_get_all_monitors(client):
    client.post(
        "/user/register",
        json={
            "username": "allmonitoruser",
            "email": "allmonitoruser@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "allmonitoruser@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response_1 = client.post(
        "/monitor/new_monitor",
        headers=headers,
        json={
            "product_link": "https://example.com/product1",
            "threshold": 500.00
        }
    )

    response_2 = client.post(
        "/monitor/new_monitor",
        headers=headers,
        json={
            "product_link": "https://example.com/product2",
            "threshold": 1000.00
        }
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    response = client.get(
        "/monitor/all",
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["product_link"] == "https://example.com/product1"
    assert data[1]["product_link"] == "https://example.com/product2"

def test_get_other_users_monitor(client):
    client.post(
        "/user/register",
        json={
            "username": "userone",
            "email": "userone@gmail.com",
            "password": "test0000"
        }
    )

    login_one = client.post(
        "/user/login",
        json={
            "email": "userone@gmail.com",
            "password": "test0000"
        }
    )

    assert login_one.status_code == 200
    token_one = login_one.json()["access_token"]

    create_response = client.post(
        "/monitor/new_monitor",
        headers={"Authorization": f"Bearer {token_one}"},
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
            "username": "usertwo",
            "email": "usertwo@gmail.com",
            "password": "test0000"
        }
    )

    login_two = client.post(
        "/user/login",
        json={
            "email": "usertwo@gmail.com",
            "password": "test0000"
        }
    )

    assert login_two.status_code == 200
    token_two = login_two.json()["access_token"]

    response = client.get(
        f"/monitor/{monitor_id}",
        headers={"Authorization": f"Bearer {token_two}"}
    )

    assert response.status_code == 404
