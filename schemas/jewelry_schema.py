from decimal import Decimal
from enum import Enum
import re
from pydantic import BaseModel, Field, field_validator

class JewelryCategory(str, Enum):
    RING = "ring"
    NECKLACE = "necklace"
    BRACELET = "bracelet"
    EARRINGS = "earrings"
    ANKLET = "anklet"
    PENDANT = "pendant"

class JewelryCreate(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    name: str = Field(min_length=1, max_length=100)
    category: JewelryCategory
    material: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)

    @field_validator("name", "material")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()

        if not re.fullmatch(
            r"^[A-Za-z0-9]+(?:[ &-][A-Za-z0-9]+)*$",
            value
    ):
            raise ValueError(
                "must contain letters, numbers, spaces, hyphens, or '&' only"
                )
        return value

class JewelryUpdate(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    name: str | None = Field(
    default=None,
    min_length=1,
    max_length=100
)
    category: JewelryCategory | None = None
    material: str | None = Field(
    default=None,
    min_length=1,
    max_length=50
)
    price: Decimal | None = Field(
    default=None,
    gt=0
)
    stock_quantity: int | None = Field(
    default=None,
    ge=0
)
    @field_validator("name", "material")
    @classmethod
    def validate_text(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not re.fullmatch(
            r"^[A-Za-z0-9]+(?:[ &-][A-Za-z0-9]+)*$",
            value
        ):
            raise ValueError(
                "must contain letters, numbers, spaces, hyphens, or '&' only"
            )

        return value

