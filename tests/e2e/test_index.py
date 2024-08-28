async def test_index_html_without_token(status_code, client):
    response = await client.get("/")
    assert response.status_code == status_code.OK.value
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
