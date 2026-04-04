from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ItemCreate(BaseModel):
    name: str
    sku: str


class Item(ItemCreate):
    id: int


_store: dict[int, Item] = {}
_next_id: int = 1


@app.get("/items")
def list_items() -> list[dict]:
    return [x.model_dump() for x in _store.values()]


@app.post("/items", status_code=201)
def create_item(body: ItemCreate) -> dict:
    global _next_id
    item = Item(id=_next_id, name=body.name, sku=body.sku)
    _store[_next_id] = item
    _next_id += 1
    return item.model_dump()


@app.get("/items/{item_id}")
def get_item(item_id: int) -> dict:
    if item_id not in _store:
        raise HTTPException(status_code=404, detail="Not found")
    return _store[item_id].model_dump()


@app.put("/items/{item_id}")
def replace_item(item_id: int, body: ItemCreate) -> dict:
    if item_id not in _store:
        raise HTTPException(status_code=404, detail="Not found")
    updated = Item(id=item_id, name=body.name, sku=body.sku)
    _store[item_id] = updated
    return updated.model_dump()


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int) -> None:
    if item_id not in _store:
        raise HTTPException(status_code=404, detail="Not found")
    del _store[item_id]
