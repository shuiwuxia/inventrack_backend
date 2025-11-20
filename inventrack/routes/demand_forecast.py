# File: routes/demand_forecast.py (MOCK UTILITY)

from typing import List, Dict, Any
from datetime import date, timedelta
import random

# Function to generate mock data. It must NOT define a router.
def create_mock_forecast(products: List[Dict[str, str]], start_date_str: str, days: int) -> List[Dict[str, Any]]:
    """
    Generates a mock forecast based on the input list of products and dates.
    This is used as a placeholder while the ML service is refactored.
    """
    forecasts = []
    
    # Ensure date conversion is robust
    try:
        start_date = date.fromisoformat(start_date_str)
    except ValueError:
        # Fallback if start_date is invalid
        start_date = date.today() + timedelta(days=1)
    
    for day_offset in range(days):
        forecast_date = start_date + timedelta(days=day_offset)
        
        for product in products:
            # Generate random integer forecast
            forecasted_units = random.randint(50, 300) 
            
            forecasts.append({
                "product_id": product["id"],
                "forecast_date": forecast_date.strftime('%Y-%m-%d'),
                # The ML model outputted floats, so we keep it as float for consistency
                "forecasted_units_sold": float(forecasted_units) 
            })
            
    return forecasts