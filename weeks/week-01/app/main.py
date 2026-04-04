from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class CommentCreate(BaseModel):
    name: str
    author: str


class Comment(CommentCreate):
    id: int


_store: dict[int, Comment] = {}
_next_id: int = 1


@app.get("/comments")
def list_comments() -> list[dict]:
    return [c.model_dump() for c in _store.values()]


@app.post("/comments", status_code=201)
def create_comment(body: CommentCreate) -> dict:
    global _next_id
    c = Comment(id=_next_id, name=body.name, author=body.author)
    _store[_next_id] = c
    _next_id += 1
    return c.model_dump()


@app.get("/comments/{comment_id}")
def get_comment(comment_id: int) -> dict:
    if comment_id not in _store:
        raise HTTPException(status_code=404, detail="Not found")
    return _store[comment_id].model_dump()
