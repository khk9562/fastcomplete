import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    response = await async_client.post(
        "/comment", json={"body": body, "post_id": post_id}
    )
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient) -> dict:
    return await create_post("Test post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict) -> dict:
    return await created_comment("Test Comment", created_post["id"], async_client)


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


@pytest.mark.anyio_backend
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post")

    assert response.status_code == 200
    assert response.json == [created_post]


@pytest.mark.anyio_backend
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "Test comment"
    post_id = created_post["id"]

    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": post_id},
    )

    assert response.status_code == 201
    assert {
        "id": 0,
        "body": body,
        "post_id": post_id,
    }.items() <= response.json().items()

    # items() 메서드는 딕셔너리의 키-값 쌍을 튜플 형태로 반환합니다.


@pytest.mark.anyio_backend
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == 200
    assert response.json() == [created_comment]


@pytest.mark.anyio_backend
async def test_get_comments_on_post_empty(
    async_client: AsyncClient, created_post: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio_backend
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}")

    assert response.status_code == 200
    assert response.json() == {
        "post": create_post,
        "comments": [created_comment],
    }
