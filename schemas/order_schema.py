from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    jewelry_id: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: str = Field(min_length=1)
    status: str = Field(min_length=1)
    items: list[OrderItemCreate] = Field(min_length=1)