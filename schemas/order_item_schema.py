from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    model_config = {
        "extra": "forbid"
    }

    order_id: str = Field(min_length=1)
    jewelry_id: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class OrderItemUpdate(BaseModel):
    model_config = {
        "extra": "forbid"
    }

    jewelry_id: str | None = Field(default=None, min_length=1)
    quantity: int | None = Field(default=None, gt=0)