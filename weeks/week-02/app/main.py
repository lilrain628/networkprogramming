from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import create_model

from coursekit.variant import load_variant

_TYPE_MAP = {"str": str, "int": int, "float": float, "bool": bool}

_v = load_variant("02")
_RESOURCE = _v["resource"]
_extra = _v["extra_field"]
_EXTRA_NAME = _extra["name"]
_EXTRA_T = _TYPE_MAP[_extra["type"]]

CreateBody = create_model(
    "CreateBody",
    name=(str, ...),
    **{_EXTRA_NAME: (_EXTRA_T, ...)},
)

_store: dict[int, dict] = {}
_next_id: int = 1

router = APIRouter()


@router.get("")
def list_all():
    return list(_store.values())


@router.post("", status_code=201)
def create_one(body: CreateBody):
    global _next_id
    row = {
        "id": _next_id,
        "name": body.name,
        _EXTRA_NAME: getattr(body, _EXTRA_NAME),
    }
    _store[_next_id] = row
    _next_id += 1
    return row


@router.get("/{rid}")
def get_one(rid: int):
    if rid not in _store:
        raise HTTPException(status_code=404, detail="Not found")
    return _store[rid]


@router.put("/{rid}")
def replace_one(rid: int, body: CreateBody):
    if rid not in _store:
        raise HTTPException(status_code=404, detail="Not found")
    row = {
        "id": rid,
        "name": body.name,
        _EXTRA_NAME: getattr(body, _EXTRA_NAME),
    }
    _store[rid] = row
    return row


@router.delete("/{rid}", status_code=204)
def delete_one(rid: int):
    if rid not in _store:
        raise HTTPException(status_code=404, detail="Not found")
    del _store[rid]


app = FastAPI()
app.include_router(router, prefix=f"/{_RESOURCE}")
