from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.get("/api/v1/other")
def get_other():
    return {"resource": "other", "data": []}
