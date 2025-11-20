# File: routes/sales.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List, Dict, Any
from datetime import date # To get the current date for SalesData
from .. import schemas, models
from ..dependencies import get_db 

router = APIRouter(
    prefix="/sales",
    tags=['Sales & Transactions']
)

DBDependency = Annotated[Session, Depends(get_db)]

@router.post("/process_bill", status_code=status.HTTP_200_OK)
def process_sale_transaction(request: schemas.ProcessSale, db: DBDependency): 
    """
    Processes a completed bill/sale:
    1. Checks inventory for stock availability.
    2. Reduces stock quantity for each item in the Inventory table.
    3. Creates a record in the SalesData table (Future-proofing/optional).
    """
    
    # 1. Verify the store exists (optional but good practice)
    shop = db.query(models.Shop).filter(models.Shop.store_id == request.store_id).first()
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Store with ID {request.store_id} not found."
        )

    # List to track sales data records created
    sales_records = [] 
    
    # --- Start Transaction ---
    # We will process all items, if any check fails, we rollback everything.
    
    try:
        for item in request.items:
            # 2. Check and reduce Inventory
            inventory_item = db.query(models.Inventory).filter(
                models.Inventory.store_id == request.store_id,
                models.Inventory.product_id == item.product_id
            ).with_for_update().first() # LOCK the row to prevent race conditions

            if not inventory_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product ID {item.product_id} not found in this shop's inventory."
                )
            
            if inventory_item.stock_quantity < item.quantity_sold:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product ID {item.product_id}. Available: {inventory_item.stock_quantity}"
                )
            
            # --- ACTION: Reduce Stock ---
            inventory_item.stock_quantity -= item.quantity_sold
            
            # 3. Create SalesData Record (using your existing model)
            # Fetch product details needed for SalesData (like price)
            product_details = db.query(models.Product).filter(
                models.Product.id == item.product_id
            ).first()
            
            if product_details:
                # Assuming the price recorded is the MSP for simplicity
                new_sale_record = models.SalesData(
                    date=date.today(),
                    store_id=request.store_id,
                    product_id=item.product_id,
                    units_sold=item.quantity_sold,
                    MSP=product_details.msp, # Using MSP from the product master
                    discount=0.00, 
                )
                db.add(new_sale_record)
                sales_records.append(new_sale_record)

        # 4. Commit all changes (Inventory updates and SalesData insertions)
        db.commit()

        return {
            "message": "Sale successfully processed and inventory updated.",
            "total_items_sold": len(request.items),
            "store_id": request.store_id,
            "total_amount": request.total_amount
        }
        
    except HTTPException as e:
        db.rollback() # Rollback on stock/ID errors
        raise e
    except Exception as e:
        db.rollback() # Rollback on any other unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during transaction: {str(e)}"
        )