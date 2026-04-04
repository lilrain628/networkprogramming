import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

from coursekit.koan import need
from coursekit.variant import load_variant

ROOT = Path(__file__).resolve().parents[3]
APP_PATH = ROOT / "weeks" / "week-02" / "app" / "main.py"


def _load_app():
    spec = importlib.util.spec_from_file_location("week02_app", APP_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.app


def test_put_updates_item():
    v = load_variant("02")
    resource = v["resource"]
    extra = v["extra_field"]
    xf = extra["name"]
    sample = {"str": "x", "int": 1, "float": 1.0, "bool": True}[extra["type"]]

    client = TestClient(_load_app())
    r = client.post(
        f"/{resource}",
        json={"name": "A", xf: sample},
    )
    need(r.status_code == 201, "POST")
    rid = r.json()["id"]

    r2 = client.put(
        f"/{resource}/{rid}",
        json={"name": "B", xf: sample},
    )
    need(r2.status_code == 200, "PUT")
    need(r2.json()["name"] == "B", "имя должно обновиться")


def test_delete_missing_returns_404():
    v = load_variant("02")
    resource = v["resource"]
    client = TestClient(_load_app())
    r = client.delete(f"/{resource}/999999")
    need(r.status_code == 404, "DELETE несуществующего — 404")
