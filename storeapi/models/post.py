from pydantic import BaseModel


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    # model_config: ConfigDict(from_attributes=True)
    id: int

    class config:
        orm_mode = (
            True  # return_value["body"] but when it fails, it will return_value.body
        )


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment] = []


"""
{
    "post": {"id": 0, "body": "This is a post"},
    "comment": [{"id": 2, "post_id": 0, "body": "This is a comment"}]
}
"""
