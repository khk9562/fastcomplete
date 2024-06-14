import logging

from fastapi import APIRouter, HTTPException

from storeapi.database import comment_table, database, post_table
from storeapi.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter()

logger = logging.getLogger(__name__)


async def find_post(post_id: int):
    # return post_table.get(post_id)
    logger.info(f"Finding post with id {post_id}")
    query = post_table.select().where(post_table.c.id == post_id)
    logger.debug(query)
    return await database.fetch_one(query)  # fetch_one / fetch_all


@router.post("/post", response_model=UserPost, tags=["posts"])
async def create_post(post: UserPostIn):
    logger.info("Creating post")
    data = post.dict()
    query = post_table.insert().values(data)
    logger.debug(query)
    last_record_id = await database.execute(query)
    await database.execute(query)
    return {**data, "id": last_record_id}
    # last_record_id = len(post_table)
    # new_post = {**data, "id": last_record_id}
    # post_table[last_record_id] = new_post
    # return new_post


@router.get("/post", response_model=list[UserPost], tags=["posts"])
async def get_all_posts():
    # return list(post_table.values())
    logger.info("Getting all posts")

    query = post_table.select()

    logger.debug(query)

    return await database.fetch_all(query)


@router.post("/comment", response_model=Comment, status_code=201, tags=["posts"])
async def create_comment(comment: CommentIn):
    logger.info("Creating comment")

    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.dict()
    query = comment_table.insert().values(data)

    logger.debug(query)

    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}
    # **data에서 **는 for desctructuring a dictionary into another dicctionary

    # last_record_id = len(comment_table)
    # new_comment = {**data, "id": last_record_id}
    # comment_table[last_record_id] = new_comment
    # return new_comment


@router.get("/post/{post_id}/comment", response_model=list[Comment], tags=["posts"])
async def get_comments_on_post(post_id: int):
    logger.info("Getting comments on post")
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    logger.debug(query)
    return await database.fetch_all(query)  # return_value["body"]
    # return [
    #     comment for comment in comment_table.values() if comment["post_id"] == post_id
    # ]


@router.get("/post/{post_id}", response_model=UserPostWithComments, tags=["posts"])
async def get_post_with_comments(post_id: int):
    logger.info("Getting post and its comments")
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
