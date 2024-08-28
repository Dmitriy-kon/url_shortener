async def test_health_check_without_token(status_code, client):
    response = await client.get("/health-check/")
    assert response.json() == {"status": "Ok"}
    assert response.status_code == status_code.OK.value

