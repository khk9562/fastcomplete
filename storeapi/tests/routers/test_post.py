import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient) -> dict:
    return await create_post("Test post", async_client)


@pytest.mark.anyio_backend
async def test_create_post(async_client: AsyncClient):
    body = "Test post"

    response = await async_client.post(
        "/post",
        json={"body": body},
    )

    assert response.status_code == 201
    assert {"id": 0, "body": body} <= response.json().items()


# write a test that attempts to create a post, but it doesn't pass a "body" key in the JSON payload.


async def test_create_post_no_body(async_client: AsyncClient):
    response = await async_client.post("/post", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
