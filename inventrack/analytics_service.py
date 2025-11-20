# File: analytics_service.py

from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any
from . import models

# --- 1. Utility Functions ---

def _get_current_period_start(period: str) -> date:
    """Calculates the start date for the current period (Daily, Weekly, Monthly, Overall)."""
    now = datetime.now()
    
    if period == 'daily':
        return datetime(now.year, now.month, now.day).date()
    elif period == 'weekly':
        # Start of current week (Monday=0)
        return (now - timedelta(days=now.weekday())).date()
    elif period == 'monthly':
        # Start of current month
        return datetime(now.year, now.month, 1).date()
    elif period == 'overall':
        # Start of all recorded time (generic historical start)
        return datetime(1970, 1, 1).date() 
    return now.date()


# --- 2. Public Service Function ---

def get_sales_analytics(db: Session, store_id: str) -> Dict[str, Any]:
    """
    Calculates all KPIs and the 30-day sales trend data for the dashboard.
    """
    results = {'store_id': store_id}
    periods = ['daily', 'weekly', 'monthly', 'overall']
    
    # Revenue expression: Units_Sold * Price (assuming Price is the DECIMAL column in SalesData)
    revenue_expr = models.SalesData.units_sold * models.SalesData.price
    
    # --- A. Calculate Simple KPIs (Daily, Weekly, Monthly, Overall) ---
    
    for period in periods:
        start_date = _get_current_period_start(period)

        # Aggregate query for the period (from start_date to today)
        metrics_query = db.query(
            func.count(models.SalesData.record_id).label('total_sales_count'),
            func.sum(models.SalesData.units_sold).label('total_units_sold'),
            func.sum(revenue_expr).label('total_revenue_inr'),
        ).filter(
            models.SalesData.store_id == store_id,
            models.SalesData.date.between(start_date, date.today())
        ).one_or_none()

        metrics = {
            'total_sales_count': float(metrics_query.total_sales_count or 0) if metrics_query else 0.0,
            'total_units_sold': float(metrics_query.total_units_sold or 0) if metrics_query else 0.0,
            'total_revenue_inr': float(metrics_query.total_revenue_inr or 0) if metrics_query else 0.0,
        }
        
        # Structure the data according to the SimpleMetric schema
        kpi_data = {
            'total_sales_count': {'value': metrics['total_sales_count'], 'unit': 'Count'},
            'total_revenue_inr': {'value': metrics['total_revenue_inr'], 'unit': 'INR'},
            'total_units_sold': {'value': metrics['total_units_sold'], 'unit': 'Units'}
        }
        
        results[f'kpis_{period}'] = kpi_data
        
    # --- B. Calculate Sales Trend Data for Graph (Last 30 Days Revenue) ---
    
    thirty_days_ago = date.today() - timedelta(days=30)
    
    # Query to get daily total revenue for the last 30 days
    trend_query = db.query(
        models.SalesData.date.label('date'),
        func.sum(revenue_expr).label('total_revenue_inr')
    ).filter(
        models.SalesData.store_id == store_id,
        models.SalesData.date >= thirty_days_ago
    ).group_by(
        models.SalesData.date
    ).order_by(
        models.SalesData.date
    ).all()

    # Convert results to Pydantic-compatible list
    results['sales_trend_data'] = [
        {
            'date': row.date.isoformat(),
            'total_revenue_inr': float(row.total_revenue_inr)
        }
        for row in trend_query
    ]
    
    return results