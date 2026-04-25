from __future__ import annotations

import subprocess
import sys
import threading
import time
from concurrent import futures
from pathlib import Path

import grpc
import requests
import uvicorn

ROOT = Path(__file__).resolve().parents[3]
WEEK08 = ROOT / "weeks" / "week-08"
PROTO_DIR = WEEK08 / "proto"
PROTO_FILE = PROTO_DIR / "service.proto"
GEN_DIR = Path(__file__).resolve().parent / "_gen"

ITERATIONS = 1000
WARMUP = 20

REST_URL = "http://127.0.0.1:8000/items"
GRPC_ADDR = "127.0.0.1:50051"


def _gen_stubs() -> None:
    GEN_DIR.mkdir(parents=True, exist_ok=True)
    if (GEN_DIR / "users" / "v1" / "service_pb2.py").exists():
        return

    cmd = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        "-I",
        str(PROTO_DIR),
        "--python_out",
        str(GEN_DIR),
        "--grpc_python_out",
        str(GEN_DIR),
        str(PROTO_FILE),
    ]
    subprocess.check_call(cmd)

    # protoc не создает __init__.py, добавим для import users.v1...
    (GEN_DIR / "users").mkdir(parents=True, exist_ok=True)
    (GEN_DIR / "users" / "v1").mkdir(parents=True, exist_ok=True)
    for p in (GEN_DIR / "users" / "__init__.py", GEN_DIR / "users" / "v1" / "__init__.py"):
        if not p.exists():
            p.write_text("", encoding="utf-8")


def _start_rest_server() -> uvicorn.Server:
    # REST сервис берём из недели 02 (resource=items для 332/s10)
    app_path = ROOT / "weeks" / "week-02" / "app" / "main.py"
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(app_path.parent))
    import main as week02_main  # type: ignore

    config = uvicorn.Config(week02_main.app, host="127.0.0.1", port=8000, log_level="warning")
    server = uvicorn.Server(config)
    t = threading.Thread(target=server.run, daemon=True)
    t.start()
    return server


def _start_grpc_server():
    sys.path.insert(0, str(GEN_DIR))
    import service_pb2  # type: ignore
    import service_pb2_grpc  # type: ignore

    class Users(service_pb2_grpc.UsersServiceServicer):
        def GetUser(self, request, context):
            return service_pb2.User(id=request.id, name="bench", email="bench@local")

        def ListUsersStream(self, request, context):
            n = request.count if request.count > 0 else 5
            for i in range(n):
                yield service_pb2.User(id=str(i), name=f"u{i}", email=f"u{i}@local")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    service_pb2_grpc.add_UsersServiceServicer_to_server(Users(), server)
    server.add_insecure_port(GRPC_ADDR)
    server.start()
    return server

def run_rest_bench():
    print("Starting REST benchmark...")
    s = requests.Session()
    for _ in range(WARMUP):
        s.get(REST_URL, timeout=5)
    start = time.perf_counter()
    for _ in range(ITERATIONS):
        s.get(REST_URL, timeout=5)
    end = time.perf_counter()
    print(f"REST: {end - start:.4f} sec")

def run_grpc_bench():
    print("Starting gRPC benchmark...")
    sys.path.insert(0, str(GEN_DIR))
    import service_pb2  # type: ignore
    import service_pb2_grpc  # type: ignore

    with grpc.insecure_channel(GRPC_ADDR) as channel:
        stub = service_pb2_grpc.UsersServiceStub(channel)
        req = service_pb2.GetUserRequest(id="1")
        for _ in range(WARMUP):
            stub.GetUser(req)
        start = time.perf_counter()
        for _ in range(ITERATIONS):
            stub.GetUser(req)
        end = time.perf_counter()
        print(f"gRPC: {end - start:.4f} sec")

if __name__ == "__main__":
    _gen_stubs()
    rest = _start_rest_server()
    grpc_srv = _start_grpc_server()
    time.sleep(0.5)
    run_rest_bench()
    run_grpc_bench()
    grpc_srv.stop(grace=1)
    rest.should_exit = True
