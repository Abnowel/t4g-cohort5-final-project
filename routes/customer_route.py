from fastapi import APIRouter,status, HTTPException
from services.customer_service import CustomerService
from schemas.customer_schema import CustomerCreate ,CustomerUpdate

router = APIRouter(prefix="/customers")

customer_service = CustomerService()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer(body: CustomerCreate):
    new_customer = customer_service.create_customer(body.model_dump())

    if new_customer == "phone_number_exists":
        raise HTTPException(
            status_code=409,
            detail="Phone number already exists"
        )

    if new_customer == "email_exists":
        raise HTTPException(
            status_code=409,
            detail="Email address already exists"
        )

    return new_customer.to_dict()


@router.get("/", status_code=status.HTTP_200_OK)
def get_customers():
    customers = customer_service.get_all_customers()
    result = []

    for customer in customers:
        result.append(customer.to_dict())

    return result

@router.get("/{customer_id}")
def get_customer(customer_id: str):
    customer = customer_service.get_customer_by_id(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer.to_dict()

@router.put("/{customer_id}")
def update_customer(customer_id: str, body: CustomerUpdate):
    updated_customer = customer_service.update_customer(
        customer_id,
        body.model_dump(exclude_unset=True)
        )

    if updated_customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return updated_customer.to_dict()

@router.delete("/{customer_id}")
def delete_customer(customer_id: str):
    deleted_customer = customer_service.delete_customer(customer_id)

    if deleted_customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    if deleted_customer == "has_orders":
        raise HTTPException(
        status_code=409,
        detail="Cannot delete customer because they have existing orders"
        )

    return {
        "message": "Customer deleted successfully"
    }