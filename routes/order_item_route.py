from fastapi import APIRouter, Body, status, HTTPException
from services.order_item_service import OrderItemService


# Creating order item router with a common prefix
router = APIRouter(prefix="/order-items")

# Creating an instance of OrderItemService
order_item_service = OrderItemService()


# Creating a new order item
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order_item(body: dict = Body(...)):

    new_order_item = order_item_service.create_order_item(body)

    if new_order_item is None:
        raise HTTPException(
            status_code=404,
            detail="Jewelry item not found"
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