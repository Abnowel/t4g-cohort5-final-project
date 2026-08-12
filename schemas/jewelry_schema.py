from pydantic import BaseModel, Field


class JewelryCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )

    category: str = Field(
        min_length=1,
        max_length=50
    )

    material: str = Field(
        min_length=1,
        max_length=50
    )

    price: float = Field(
        gt=0
    )

    stock_quantity: int = Field(
        ge=0
    )

    model_config = {
        "extra": "forbid"
    }