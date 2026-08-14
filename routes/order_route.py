from fastapi import APIRouter, status , HTTPException
from services.order_service import OrderService
from schemas.order_schema import OrderCreate , OrderUpdate


# Creating order router with a common prefix
router = APIRouter(prefix="/orders")

# Creating an instance of OrderService
order_service = OrderService()

# Creating a new order
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(body: OrderCreate):

    new_order = order_service.create_order(
        body.model_dump()
        )

    if new_order == "customer_not_found":
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if new_order is None:
        raise HTTPException(
            status_code=404,
            detail = "Jewelry item not found"
        )

    return new_order.to_dict()

# Get all orders
@router.get("/")
def get_orders():
    orders = order_service.get_all_orders()

    result = []

    for order in orders:
        result.append(order.to_dict())

    return result

# Get one order by ID
@router.get("/{order_id}")
def get_order_by_id(order_id: str):

    order = order_service.get_order_by_id(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order.to_dict()

# Update an existing order
@router.put("/{order_id}")
def update_order(
    order_id: str, 
    body: OrderUpdate
    ):

    updated_order = order_service.update_order(
        order_id,
        body.model_dump()
    )

    if updated_order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return updated_order.to_dict()

# Delete an existing order
@router.delete("/{order_id}")
def delete_order(order_id: str):

    deleted_order = order_service.delete_order(order_id)

    if deleted_order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if deleted_order == "has_order_items":
        raise HTTPException(
        status_code=409,
        detail="Cannot delete order because it has existing order items"
    )

    return {
        "message": "Order deleted successfully"
    }