from fastapi import APIRouter, Body, status
from services.customer_service import CustomerService

router = APIRouter()

customer_service = CustomerService()

@router.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(body: dict = Body(...)):
    new_customer = customer_service.create_customer(body)

    return new_customer.to_dict()