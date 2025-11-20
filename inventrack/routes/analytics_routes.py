# File: routes/analytics_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from inventrack.dependencies import get_db
from inventrack.schemas import SalesAnalyticsResponse # Import the response schema
from inventrack.analytics_service import get_sales_analytics
from inventrack import models # Needed for store existence check

router = APIRouter(
    prefix="/analytics",
    tags=['Sales Analytics Dashboard']
)

DBDependency = Annotated[Session, Depends(get_db)]

@router.get(
    "/{store_id}", 
    response_model=SalesAnalyticsResponse,
    status_code=status.HTTP_200_OK
)
def get_dashboard_analytics(store_id: str, db: DBDependency):
    """
    Retrieves all key sales metrics (Revenue, Sales Count, Units Sold) 
    for the current Daily, Weekly, Monthly, and Overall periods, 
    plus time-series data for the sales trend graph.
    """
    
    # 1. Verify the store exists
    shop = db.query(models.Shop).filter(models.Shop.store_id == store_id).first()
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Store ID {store_id} not found."
        )

    # 2. Call the service function to compute all metrics
    try:
        analytics_data = get_sales_analytics(db, store_id)
        return analytics_data
    except Exception as e:
        # Catch exceptions during query execution or processing
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process sales analytics: {str(e)}"
        )