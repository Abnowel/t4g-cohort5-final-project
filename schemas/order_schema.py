from enum import Enum
from pydantic import BaseModel, Field

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderItemInOrder(BaseModel):
    model_config ={
        "extra":"forbid"
    }
    jewelry_id: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    model_config ={
        "extra": "forbid"
    }
    customer_id: str = Field(min_length=1)
    items: list[OrderItemInOrder] = Field(min_length=1)

class OrderUpdate(BaseModel):
    model_config = {
        "extra": "forbid"
    }

    status: OrderStatus