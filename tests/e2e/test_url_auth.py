async def test_url_get_all_auth(status_code, auth_client):
    response = await auth_client.get("/url/all")
    assert response.status_code == status_code.OK.value


async def test_insert_url_auth(status_code, auth_client):
    data = {"url": "https://google.com"}
    response = await auth_client.post("/url/insert", json=data)
    assert response.status_code == status_code.OK.value
    assert set(response.json()) == {"urlid", "url", "short_url", "user_id", "clics"}

    new_data = {"url": "https://google.com"}
    response2 = await auth_client.post("/url/insert", json=new_data)
    assert response2.status_code == status_code.CONFLICT.value


async def test_change_url_auth(status_code, auth_client):
    data = {"url": "https://google2.com"}
    response = await auth_client.post("/url/insert", json=data)
    old_short_url = response.json().get("short_url")
    url_id = response.json().get("urlid")

    response2 = await auth_client.patch(f"/url/change/?url_id={url_id}")
    new_short_url = response2.json().get("short_url")

    wrong_response = await auth_client.patch(f"/url/change/?url_id={url_id+9999}")

    assert new_short_url != old_short_url
    assert response2.status_code == status_code.OK.value
    assert wrong_response.status_code == status_code.NOT_FOUND.value


async def test_delete_url_auth(status_code, auth_client):
    data = {"url": "https://google3.com"}
    response = await auth_client.post("/url/insert", json=data)
    url_id = response.json().get("urlid")

    response2 = await auth_client.delete(f"/url/delete/?url_id={url_id}")
    response_wrong = await auth_client.delete(f"/url/delete/?url_id={url_id+9999}")

    assert response2.status_code == status_code.OK.value
    assert response_wrong.status_code == status_code.NOT_FOUND.value
