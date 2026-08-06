from fastapi import APIRouter, Body, status, HTTPException
from services.customer_service import CustomerService

router = APIRouter(prefix="/customers")

customer_service = CustomerService()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer(body: dict = Body(...)):
    new_customer = customer_service.create_customer(body)

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