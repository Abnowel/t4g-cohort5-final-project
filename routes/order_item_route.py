from fastapi import APIRouter, status, HTTPException
from services.order_item_service import OrderItemService
from schemas.order_item_schema import OrderItemCreate,OrderItemUpdate


# Creating order item router with a common prefix
router = APIRouter(prefix="/order-items")

# Creating an instance of OrderItemService
order_item_service = OrderItemService()


# Creating a new order item
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order_item(body: OrderItemCreate):

    new_order_item = order_item_service.create_order_item(
        body.model_dump()
    )

    if new_order_item == "order_not_found":
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if new_order_item == "jewelry_not_found":
        raise HTTPException(
            status_code=404,
            detail= "Jewelry item not found"
        )

    if new_order_item == "insufficient_stock":
        raise HTTPException(
            status_code=409,
            detail="Insufficient stock"
        )

    return new_order_item.to_dict()

# Get all order items
@router.get("/")
def get_order_items():
    order_items = order_item_service.get_all_order_items()

    result = []

    for order_item in order_items:
        result.append(order_item.to_dict())

    return result

# Get one order item by ID
@router.get("/{order_item_id}")
def get_order_item_by_id(order_item_id: str):

    order_item = order_item_service.get_order_item_by_id(
        order_item_id
    )

    if order_item is None:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    return order_item.to_dict()

# Update an existing order item
@router.put("/{order_item_id}")
def update_order_item(
    order_item_id: str,
    body: OrderItemUpdate
):

    updated_order_item = order_item_service.update_order_item(
        order_item_id,
        body.model_dump(exclude_unset=True)
    )

    if updated_order_item == "insufficient_stock":
        raise HTTPException(
            status_code=409,
            detail="Insufficient stock"
        )
    
    if updated_order_item is None:
        raise HTTPException(
            status_code=404,
            detail="Order item or jewelry item not found"
        )

    return updated_order_item.to_dict()

# Delete an existing order item
@router.delete("/{order_item_id}")
def delete_order_item(order_item_id: str):

    deleted_order_item = order_item_service.delete_order_item(
        order_item_id
    )

    if deleted_order_item is None:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    return {
        "message": "Order item deleted successfully"
    }