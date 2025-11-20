# File: routes/ml_data_access.py

from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any, Union
import json
from pathlib import Path

# --- Correct base path ---
BASE_DIR = Path(__file__).resolve().parent.parent  # go up to 'inventrack'
RECOMMENDATION_FILE = BASE_DIR / "recommendar2_api_output.txt"
RESTOCK_FILE = BASE_DIR / "analytics_output.txt"

router = APIRouter(
    prefix="/ml-data",
    tags=['External ML Outputs']
)

# --- Endpoint 1: Product Recommendations ---
@router.get(
    "/recommendations",
    response_model=Union[Dict[str, Any], List[Dict[str, Any]]],
    status_code=status.HTTP_200_OK
)
def get_product_recommendations():
    print(f"Looking for recommendation file at: {RECOMMENDATION_FILE.resolve()}")

    if not RECOMMENDATION_FILE.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation file '{RECOMMENDATION_FILE}' not found. Ensure the model run is complete."
        )

    try:
        with open(RECOMMENDATION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading or processing {RECOMMENDATION_FILE}: {str(e)}"
        )

# --- Endpoint 2: Restock Recommendations ---
@router.get(
    "/restock-status",
    response_model=Union[Dict[str, Any], List[Dict[str, Any]]],
    status_code=status.HTTP_200_OK
)
def get_restock_status():
    print(f"Looking for restock file at: {RESTOCK_FILE.resolve()}")

    if not RESTOCK_FILE.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restock file '{RESTOCK_FILE}' not found. Ensure the model run is complete."
        )

    try:
        # ✅ Read as JSON, not joblib
        with open(RESTOCK_FILE, "r", encoding="utf-8") as f:
            restock_data = json.load(f)
        return restock_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading or processing {RESTOCK_FILE}: {str(e)}"
        )
