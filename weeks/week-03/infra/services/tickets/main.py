from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.get("/api/tickets")
def get_tickets():
    return {"resource": "tickets", "data": []}
