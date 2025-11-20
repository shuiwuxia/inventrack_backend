# File: main.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from inventrack import models
from inventrack.database import engine 
from inventrack.dependencies import get_db 
# Import all routers. Note: demand_routes contains the actual endpoint.
# File: main.py (MODIFIED)
# ...
from inventrack.routes import auth, products, inventory, sales, demand_routes, ml_data_access, analytics_routes, consumer_auth_routes 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include all routers
app.include_router(sales.router) 
app.include_router(inventory.router) 
app.include_router(auth.router)
app.include_router(products.router) 
app.include_router(demand_routes.router)
app.include_router(ml_data_access.router)
app.include_router(analytics_routes.router) 
app.include_router(consumer_auth_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to InvenTrack API"}
origins = [

    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)