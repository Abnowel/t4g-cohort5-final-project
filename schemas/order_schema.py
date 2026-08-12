from enum import Enum
from pydantic import BaseModel, Field

class OrderStatus(str, Enum):
    pending = "pending"
    completed = "completed"


class OrderItemCreate(BaseModel):
    jewelry_id: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    model_config ={
        "extra": "forbid"
    }
    customer_id: str = Field(min_length=1)
    items: list[OrderItemCreate] = Field(min_length=1)