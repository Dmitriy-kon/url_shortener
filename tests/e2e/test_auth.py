import asyncio


async def test_auth_reg_without_token(status_code, client):
    data = {"username": "test2user2", "password": "test2password2"}
    data2 = {"username": "test2", "password": "test"}
    data3 = {"username": "test2user2", "password": "test2password2"}

    response = await client.post("/auth/signup", data=data)
    response2 = await client.post("/auth/signup", data=data2)
    response3 = await client.post("/auth/signup", data=data3)

    assert response.json() == {"message": "user created"}
    assert response.status_code == status_code.OK.value

    assert response2.status_code == status_code.UNSUPPORTED_ENTITY.value
    assert response3.status_code == status_code.CONFLICT.value


async def test_auth_login_without_token(status_code, client):
    data = {"username": "test2user2new", "password": "test2password2"}
    await client.post("/auth/signup", data=data)

    response1 = await client.post("/auth/login", data=data)
    await asyncio.sleep(1)
    response2 = await client.post("/auth/login", data=data)

    assert response1.status_code == status_code.OK.value
    assert response1.headers["Content-Type"] == "application/json"
    assert set(response1.json()) == {"username", "urls"}

    token1 = response1.cookies.get("access_token").replace("Bearer ", "")
    token2 = response2.cookies.get("access_token").replace("Bearer ", "")

    assert token1 != token2, "Tokens should be different"
