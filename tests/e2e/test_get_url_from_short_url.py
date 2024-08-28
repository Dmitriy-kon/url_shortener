async def test_get_url_from_short_url(status_code, client, auth_client):
    url = "https://google20.com"
    data = {"url": url}
    response = await auth_client.post("/url/insert", json=data)

    short_url = response.json().get("short_url")

    response_without_auth = await client.get(f"/t/?short={short_url}")
    response_auth = await auth_client.get(f"/t/?short={short_url}")

    assert response_without_auth.status_code == status_code.REDIRECT.value
    assert response_without_auth.headers["location"] == f"{url}/"

    assert response_auth.status_code == status_code.REDIRECT.value
    assert response_auth.headers["location"] == f"{url}/"
