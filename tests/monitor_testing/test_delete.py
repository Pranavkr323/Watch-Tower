def test_delete_monitor(client):
    client.post(
        "/user/register",
        json={
            "username": "deleteuser",
            "email": "deleteuser@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "deleteuser@gmail.com",
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

    delete_response = client.delete(
        f"/monitor/{monitor_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Monitor deleted successfully"

    get_response = client.get(
        f"/monitor/{monitor_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert get_response.status_code == 404

def test_delete_nonexistent_monitor(client):
    client.post(
        "/user/register",
        json={
            "username": "delete404",
            "email": "delete404@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "delete404@gmail.com",
            "password": "test0000"
        }
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.delete(
        "/monitor/9999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Monitor not found!"


def test_delete_unauthorized(client):
    client.post(
        "/user/register",
        json={
            "username": "deleteowner",
            "email": "deleteowner@gmail.com",
            "password": "test0000"
        }
    )

    login_response = client.post(
        "/user/login",
        json={
            "email": "deleteowner@gmail.com",
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
            "username": "deleteother",
            "email": "deleteother@gmail.com",
            "password": "test0000"
        }
    )

    other_login = client.post(
        "/user/login",
        json={
            "email": "deleteother@gmail.com",
            "password": "test0000"
        }
    )

    assert other_login.status_code == 200
    other_token = other_login.json()["access_token"]

    response = client.delete(
        f"/monitor/{monitor_id}",
        headers={
            "Authorization": f"Bearer {other_token}"
        }
    )

    assert response.status_code == 404
