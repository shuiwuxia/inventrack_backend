# File: routes/demand_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List, Dict, Any
from sqlalchemy.orm import Session
from inventrack.dependencies import get_db
from inventrack import schemas, models
# Correctly import the mock utility function
from .demand_forecast import create_mock_forecast 

router = APIRouter(
    prefix="/forecast",
    tags=['Demand Forecasting (Dynamic)']
)

DBDependency = Annotated[Session, Depends(get_db)]

@router.post(
    "/demand", 
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK
)
def get_demand_forecast_dynamic(
    request: schemas.DemandForecastRequest,
    db: DBDependency
):
    """
    DYNAMIC ENDPOINT: Triggers the ML prediction based on the specific 
    Store ID, User ID, and the list of Product IDs provided in the request body.
    
    NOTE: Currently returns mock data. This function will be updated to call 
    the refactored forecasting_service when ready.
    """
    
    # --- STEP 1: VERIFY CONTEXT (Required by the dynamic design) ---
    shop = db.query(models.Shop).filter(models.Shop.store_id == request.store_id).first()
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Store ID {request.store_id} not found."
        )

    # --- STEP 2: MOCK RETURN (Using the corrected utility function) ---
    
    # The Mock function expects a list of product objects like [{"id": "P0001"}, ...]
    products_for_mock = [{"id": pid} for pid in request.product_ids]
    
    # Call the mock utility with the request data
    return create_mock_forecast(
        products=products_for_mock,
        start_date_str=request.forecast_start_date,
        days=request.forecast_days
    )