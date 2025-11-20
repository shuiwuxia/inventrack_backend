from fastapi import FastAPI
from main import app   # <-- import the FastAPI instance

import os

@app.get("/ml_data/restock-status")
def test_path():
    base = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(base)
    path = os.path.join(root, "analytics_output.txt")
    return {"exists": os.path.exists(path), "path": path}
