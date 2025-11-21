# File: inventrack/schemas.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date

class ForecastPoint(BaseModel):
    date: str
    forecast: float
# --- User Schemas (Mapped to 'users' table) ---

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str  
    role: str    
    phone: str
    location: Optional[str] = None

class UserLogin(BaseModel):
    identifier: str  # Accepts either email or phone
    password: str

class User(BaseModel):
    id: int # Maps to user_id
    full_name: str
    email: str
    role: str
    phone: str
    location: Optional[str] = None
    
    class Config:
        from_attributes = True

# --- Shopkeeper Schema (Mapped to 'users' & 'shops') ---

class ShopkeeperCreate(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    location: Optional[str] = None
    shop_name: str
    business_verification_id: Optional[str] = None
    address: str      # Maps to Address_Line1
    shop_phone: Optional[str] = None
    store_type: Optional[str] = None


# --- Product Schemas (Mapped to 'products' table) ---
# --- Product Schemas (Mapped to 'products' table) ---

class ProductCreate(BaseModel):
    product_name: str
    category: str
    subcategory: str
    mrp: float
    msp: float
    stock_quantity: int

class Product(BaseModel):
    product_id: str = Field(..., alias="id")
    product_name: str = Field(..., alias="name")
    category: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    mrp: Optional[float] = None
    msp: Optional[float] = None
    unit_of_measure: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    mrp: Optional[float] = None
    msp: Optional[float] = None
    stock_quantity: Optional[int] = None

# --- Inventory Schemas (Mapped to 'inventory' table) ---

# Schema for returning a product WITH its stock level (using inheritance)
class InventoryProduct(Product): 
    qty: int            # FIX: Changed from 'stock_quantity' to 'qty'
    
    class Config(Product.Config):
        pass 

# --- Sales Schemas ---

class SaleItem(BaseModel):
    product_id: str
    product_name: str 
    quantity_sold: int 

class ProcessSale(BaseModel):
    store_id: str
    user_id: int       
    total_amount: float
    items: List[SaleItem]

# --- Demand Forecasting Schemas (NEW) ---

class DemandForecastRequest(BaseModel):
    """Schema for the dynamic request that powers the ML prediction."""
    store_id: str             # The ID of the store being managed
    user_id: int              # The ID of the currently logged-in user
    product_ids: List[str]    # The list of products to generate forecasts for
    forecast_start_date: str  # YYYY-MM-DD format
    forecast_days: int = 7    # Default to 7 days

# --- Demand Forecasting Schemas ---

class DemandForecastRequest(BaseModel):
    store_id: str
    user_id: int
    product_ids: List[str]
    forecast_start_date: str
    forecast_days: int = 7

# --- Sales Analytics Schemas (Dashboard KPIs) ---

class SimpleMetric(BaseModel):
    """Schema for a single KPI value."""
    value: float = Field(..., description="The current period value.")
    unit: str = Field(..., description="The unit of the metric (e.g., 'INR', 'Units', 'Count').")
    
class TimePeriodKPI(BaseModel):
    """Schema grouping all KPIs for a specific time window."""
    total_sales_count: SimpleMetric
    total_revenue_inr: SimpleMetric
    total_units_sold: SimpleMetric
    
class SalesTrendDataPoint(BaseModel):
    """A single data point for the sales trend graph."""
    revenue_date: Union[date, str] = Field(..., description="Date of the revenue data point.")
    total_revenue_inr: float = Field(..., description="Total revenue for that specific period.")

class SalesAnalyticsResponse(BaseModel):
    """The full dashboard response containing all simplified metrics and graph data."""
    store_id: str
    
    # KPIs for different time granularities
    kpis_daily: TimePeriodKPI
    kpis_weekly: TimePeriodKPI
    kpis_monthly: TimePeriodKPI
    kpis_overall: TimePeriodKPI
    # Data for the graph
    sales_trend_data: List[SalesTrendDataPoint]
    forecast_trend: List[ForecastPoint] = []
class ConsumerCreate(BaseModel):
    full_name: str
    email_id: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    password: str # Plaintext password sent by the user

class Consumer(BaseModel):
    consumer_id: int
    full_name: str
    email_id: str
    phone_number: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True

