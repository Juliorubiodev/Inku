from fastapi import FastAPI

app = FastAPI(title="List Service")

# Example in-memory list
items = [
    {"id": 1, "name": "Item A"},
    {"id": 2, "name": "Item B"},
]

@app.get("/api/list")
def get_items():
    return {"items": items}

@app.get("/")
def root():
    return {"message": "List Service is running!"}
