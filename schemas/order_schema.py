from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    jewelry_id: str
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: str
    status: str
    items: list[OrderItemCreate]