import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code",[
    ("kor@pes.ru", "kotopes", 200),
    ("kor@pes.ru", "kot0pes", 409),
    ("abcde", "kotopes", 422)
])
async def test_register(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/v1/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("test@test.com", "test", 200),
    ("artem@example.com", "artem", 200),
    ("wrong@example.com", "wrong", 401)
])
async def test_authenticated(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/v1/auth/authenticated", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code
