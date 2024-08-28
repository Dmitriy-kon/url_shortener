async def test_url_get_all_without_token(status_code, client):
    response = await client.get("/url/all")
    assert response.status_code == status_code.UNAUTHORIZED.value
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers.get("WWW-Authenticate") == "Bearer"


async def test_insert_url_without_token(status_code, client):
    response = await client.post("/url/insert")
    assert response.status_code == status_code.UNAUTHORIZED.value
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers.get("WWW-Authenticate") == "Bearer"


async def test_change_url_without_token(status_code, client):
    response = await client.patch("/url/change/")
    assert response.status_code == status_code.UNAUTHORIZED.value
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers.get("WWW-Authenticate") == "Bearer"


async def test_delete_url_without_token(status_code, client):
    response = await client.delete("/url/delete/")
    assert response.status_code == status_code.UNAUTHORIZED.value
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers.get("WWW-Authenticate") == "Bearer"
